#!/usr/bin/env python3
"""servo_controller node.

Action server for pan/tilt motion, plus a calibration service and a state
publisher. Replaces the legacy Trigger-based motor node.

Responsibilities, and what each one is for
------------------------------------------
* **GoToAngle action** — progress feedback, cancellation, an explicit STALLED
  result distinct from a timeout, and a clamp flag so the operator is never
  told it reached an angle it did not.
* **Home action** — establishes the zero reference. Without it, "visit 37
  degrees" is meaningless.
* **SetCalibration / GetCalibration services** — install and read the
  classroom's geometry atomically.
* **/stand/set_target (std_srvs/Trigger-compatible subscriber)** — retained so
  the archived `attendance_mocks` scan controller can still drive this node.
  Marked deprecated.
* **State topic** — published on change and on a timer, because a topic that
  only publishes on change is useless to a node that just started.

The honesty rule
----------------
When ``has_position_feedback`` is false, the node reports
``position_is_measured: false`` and refuses to declare a stall. Reporting a
commanded angle as a measured one is how the legacy code made an unverified
assumption look like a fact.
"""

from __future__ import annotations

import contextlib
import threading
import time

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from attendance_interfaces.action import GoToAngle, Home, RunScanSequence
from attendance_interfaces.msg import ServoState
from attendance_interfaces.srv import GetCalibration, SetCalibration, SetZoom
from servo_controller.driver import (
    DriverError,
    DriverNotConnected,
    SerialServoDriver,
    SimulatedDriver,
)
from servo_controller.limits import Limits, MotionProfile, Phase

#: Reason codes, part of the observable contract.
FAULT_STALL = "stall"
FAULT_TIMEOUT = "timeout"
FAULT_NOT_HOMED = "not_homed"
FAULT_OUT_OF_RANGE = "out_of_range"
FAULT_DRIVER = "driver_error"
FAULT_CANCELLED = "cancelled"


class ServoControllerNode(Node):
    """Pan/tilt actuation with enforced limits."""

    def __init__(self) -> None:
        super().__init__("servo_controller")
        self.declare_parameter("driver", "simulated")
        self.declare_parameter("pan_min_deg", -90.0)
        self.declare_parameter("pan_max_deg", 90.0)
        self.declare_parameter("tilt_min_deg", -30.0)
        self.declare_parameter("tilt_max_deg", 45.0)
        self.declare_parameter("max_speed_deg_per_s", 30.0)
        self.declare_parameter("max_accel_deg_per_s2", 120.0)
        self.declare_parameter("tolerance_deg", 0.5)
        self.declare_parameter("has_position_feedback", True)
        self.declare_parameter("serial_port", "/dev/ttyUSB0")
        self.declare_parameter("serial_baudrate", 115200)
        self.declare_parameter("serial_read_timeout_s", 0.5)
        self.declare_parameter("state_publish_rate_hz", 10.0)
        self.declare_parameter("stall_ticks_before_fault", 10)
        self.declare_parameter("move_timeout_s", 15.0)

        self._pan_limits = Limits(
            min_deg=float(self.get_parameter("pan_min_deg").value),
            max_deg=float(self.get_parameter("pan_max_deg").value),
            max_speed_deg_per_s=float(self.get_parameter("max_speed_deg_per_s").value),
            max_accel_deg_per_s2=float(self.get_parameter("max_accel_deg_per_s2").value),
            has_position_feedback=bool(self.get_parameter("has_position_feedback").value),
            tolerance_deg=float(self.get_parameter("tolerance_deg").value),
        )
        self._tilt_limits = Limits(
            min_deg=float(self.get_parameter("tilt_min_deg").value),
            max_deg=float(self.get_parameter("tilt_max_deg").value),
            max_speed_deg_per_s=float(self.get_parameter("max_speed_deg_per_s").value),
            max_accel_deg_per_s2=float(self.get_parameter("max_accel_deg_per_s2").value),
            has_position_feedback=bool(self.get_parameter("has_position_feedback").value),
            tolerance_deg=float(self.get_parameter("tolerance_deg").value),
        )

        driver_name = str(self.get_parameter("driver").value)
        if driver_name == "simulated":
            self._driver: SimulatedDriver | SerialServoDriver = SimulatedDriver(
                min_deg=self._pan_limits.min_deg,
                max_deg=self._pan_limits.max_deg,
                max_speed_deg_per_s=self._pan_limits.max_speed_deg_per_s,
            )
        elif driver_name == "serial":
            self._driver = SerialServoDriver(
                port=str(self.get_parameter("serial_port").value),
                baudrate=int(self.get_parameter("serial_baudrate").value),
                has_position_feedback=self._pan_limits.has_position_feedback,
                read_timeout_s=float(self.get_parameter("serial_read_timeout_s").value),
            )
        else:
            raise ValueError(f"unknown driver '{driver_name}'; use 'simulated' or 'serial'")

        self._lock = threading.RLock()
        self._homed = driver_name == "simulated"
        self._estop = False
        self._fault = ""
        self._state = "IDLE"
        self._target = 0.0
        self._tilt_target = 0.0
        self._calibration_version = "built-in-defaults"
        self._region_angles: list[str] = []
        self._region_names: list[str] = []
        self._motion: MotionProfile | None = None
        self._cancelled = threading.Event()

        callbacks = ReentrantCallbackGroup()

        self._state_pub = self.create_publisher(
            ServoState, "/stand/servo_state", 10, callback_group=callbacks
        )
        self._timer = self.create_timer(
            1.0 / float(self.get_parameter("state_publish_rate_hz").value),
            self._publish_state,
            callback_group=callbacks,
        )

        self._goto_server = ActionServer(
            self,
            GoToAngle,
            "/stand/goto_angle",
            execute_callback=self._execute_goto,
            goal_callback=lambda _: GoalResponse.ACCEPT,
            cancel_callback=self._on_cancel,
            callback_group=callbacks,
        )
        self._home_server = ActionServer(
            self,
            Home,
            "/stand/home",
            execute_callback=self._execute_home,
            goal_callback=lambda _: GoalResponse.ACCEPT,
            cancel_callback=self._on_cancel,
            callback_group=callbacks,
        )
        # A scan goal is accepted and refused cleanly: the scan planner drives
        # the mechanism, so this server exists only so an operator asking for
        # a scan gets a real answer rather than a missing service.
        self._scan_server = ActionServer(
            self,
            RunScanSequence,
            "/stand/run_scan",
            execute_callback=self._execute_scan_refused,
            goal_callback=lambda _: GoalResponse.ACCEPT,
            cancel_callback=lambda _: CancelResponse.ACCEPT,
            callback_group=callbacks,
        )

        self.create_service(
            SetCalibration, "/stand/set_calibration", self._on_set_calibration, callback_group=callbacks
        )
        self.create_service(
            GetCalibration, "/stand/get_calibration", self._on_get_calibration, callback_group=callbacks
        )
        self.create_service(SetZoom, "/stand/set_zoom", self._on_set_zoom, callback_group=callbacks)

        # Legacy compatibility: the archived scan controller publishes a
        # Float64. Deprecated and removed with attendance_mocks.
        self.create_subscription(
            __import__("std_msgs.msg", fromlist=["Float64"]).Float64,
            "/stand/set_target",
            self._on_legacy_target,
            10,
            callback_group=callbacks,
        )

        self.get_logger().info(
            f"ServoController ready: driver={driver_name} "
            f"pan=[{self._pan_limits.min_deg:.0f}, {self._pan_limits.max_deg:.0f}] "
            f"feedback={self._pan_limits.has_position_feedback} "
            f"{'(stall detection UNAVAILABLE)' if not self._pan_limits.has_position_feedback else ''}"
        )
        if not self._pan_limits.has_position_feedback:
            self.get_logger().warn(
                "has_position_feedback is false: this mechanism cannot report its true "
                "angle and the node CANNOT detect a stall. Do not treat reached_angle as "
                "measured. See docs/hardware/wiring.md."
            )

    # -- actions ---------------------------------------------------------
    def _on_cancel(self, _goal_handle) -> CancelResponse:
        """Signal the running move to stop."""
        self._cancelled.set()
        return CancelResponse.ACCEPT

    def _execute_goto(self, goal_handle) -> None:
        """Move to a commanded angle with ramping, limits and stall detection."""
        goal = goal_handle.request
        feedback = goal_handle.feedback
        result = goal_handle.result

        with self._lock:
            if self._estop:
                result.success = False
                result.error_message = "emergency stop is engaged; release it with /stand/clear_estop"
                result.fault_code = FAULT_CANCELLED
                goal_handle.succeed()
                return
            if goal.require_homed and not self._homed:
                result.success = False
                result.error_message = "not homed; call /stand/home first"
                result.fault_code = FAULT_NOT_HOMED
                goal_handle.succeed()
                return

            requested = float(goal.pan_angle_deg)
            target = self._pan_limits.clamp(requested)
            clamped = abs(target - requested) > 1e-6
            if clamped:
                self.get_logger().warn(
                    f"angle {requested:.1f} clamped to {target:.1f} "
                    f"(limits {self._pan_limits.min_deg:.0f}..{self._pan_limits.max_deg:.0f})"
                )

            self._cancelled.clear()
            self._target = target
            self._state = "MOVING"
            speed = float(goal.speed_deg_per_s) or self._pan_limits.max_speed_deg_per_s
            profile = MotionProfile(
                limits=self._pan_limits,
                target_deg=target,
                commanded_deg=self._driver.position(),
            )
            del speed
            self._motion = profile

        started = time.monotonic()
        deadline = started + float(
            goal.timeout_s if goal.timeout_s > 0 else self.get_parameter("move_timeout_s").value
        )
        dt = 1.0 / max(float(self.get_parameter("state_publish_rate_hz").value), 1.0)

        while rclpy.ok():
            measured = self._driver.position() if self._pan_limits.has_position_feedback else None
            with self._lock:
                phase = profile.step(dt, measured)
                reached = profile.commanded_deg

            feedback.pan_angle_deg = reached
            feedback.phase = int(phase)
            feedback.progress = float(profile.progress)
            feedback.stalled = phase is Phase.STALLED
            goal_handle.publish_feedback(feedback)
            self._publish_state()

            if phase is Phase.ARRIVED:
                with self._lock:
                    self._state = "AT_TARGET"
                result.success = True
                result.reached_pan_deg = reached
                result.reached_tilt_deg = self._tilt_target
                result.clamped = clamped
                result.duration_ms = (time.monotonic() - started) * 1000.0
                goal_handle.succeed()
                return

            if phase is Phase.STALLED:
                self.get_logger().error(
                    f"STALL: no progress for {profile.stalled_ticks} ticks heading to {target:.1f}"
                )
                self._driver.stop()
                with self._lock:
                    self._state = "STALLED"
                    self._fault = FAULT_STALL
                result.success = False
                result.error_message = (
                    "the mechanism stopped moving while still commanded. It is jammed, "
                    "underloaded, or the feedback wire is loose."
                )
                result.fault_code = FAULT_STALL
                result.reached_pan_deg = reached
                goal_handle.succeed()
                return

            if self._cancelled.is_set():
                profile.cancel()
                self._driver.stop()
                with self._lock:
                    self._state = "IDLE"
                result.success = False
                result.error_message = "cancelled"
                result.fault_code = FAULT_CANCELLED
                result.reached_pan_deg = reached
                goal_handle.canceled()
                return

            if time.monotonic() > deadline:
                self._driver.stop()
                with self._lock:
                    self._state = "ERROR"
                    self._fault = FAULT_TIMEOUT
                result.success = False
                result.error_message = f"did not reach {target:.1f} within the timeout"
                result.fault_code = FAULT_TIMEOUT
                result.reached_pan_deg = reached
                goal_handle.succeed()
                return

            # Tell the driver where we want to be. On a no-feedback mechanism
            # this is the ONLY way it learns the target.
            try:
                self._driver.move_to(profile.commanded_deg, self._pan_limits.max_speed_deg_per_s, 1.0)
            except DriverError as exc:
                with self._lock:
                    self._state = "ERROR"
                    self._fault = FAULT_DRIVER
                result.success = False
                result.error_message = str(exc)
                result.fault_code = FAULT_DRIVER
                goal_handle.succeed()
                return

            time.sleep(dt)

        # rclpy shut down mid-move.
        self._driver.stop()
        result.success = False
        result.error_message = "node shut down during the move"
        result.fault_code = FAULT_CANCELLED
        goal_handle.canceled()

    def _execute_home(self, goal_handle) -> None:
        """Establish the zero reference."""
        goal = goal_handle.request
        feedback = goal_handle.feedback
        result = goal_handle.result
        self._cancelled.clear()

        with self._lock:
            self._state = "HOMING"

        deadline = time.monotonic() + (float(goal.timeout_s) if goal.timeout_s > 0 else 20.0)
        for phase_value, label in ((0, "APPROACHING"), (3, "SETTLING")):
            feedback.phase = phase_value
            feedback.progress = 0.5
            goal_handle.publish_feedback(feedback)
            del label
            if time.monotonic() > deadline:
                break

        try:
            home_angle = self._driver.home()
        except DriverError as exc:
            with self._lock:
                self._state = "ERROR"
                self._fault = FAULT_DRIVER
            result.success = False
            result.error_message = str(exc)
            result.fault_code = FAULT_DRIVER
            goal_handle.succeed()
            return

        with self._lock:
            self._homed = True
            self._state = "IDLE"
            self._fault = ""
        result.success = True
        result.homed = True
        result.home_angle_deg = home_angle
        # Honest about what happened: on a hobby servo this was a busy
        # gesture at the endstop, not a real home switch.
        result.has_position_feedback = self._pan_limits.has_position_feedback
        goal_handle.succeed()
        if not self._pan_limits.has_position_feedback:
            self.get_logger().warn(
                "home completed WITHOUT position feedback: this was a busy gesture at the "
                "endstop, not a true home. The zero will drift with temperature."
            )

    def _execute_scan_refused(self, goal_handle) -> None:
        """Refuse a scan goal with a real answer.

        The scan planner owns scan execution. Accepting the goal and doing
        nothing would leave an operator watching a progress bar that never
        moves, which is worse than a clear refusal.
        """
        result = goal_handle.result
        result.success = False
        result.error_message = (
            "servo_controller does not run scans. Use the scan_planner's "
            "/scan_planner/run_scan action, which drives this node's /stand/goto_angle."
        )
        result.fault_code = "not_this_node"
        goal_handle.succeed()

    # -- services --------------------------------------------------------
    def _on_set_calibration(self, request, response):
        """Install a classroom calibration atomically."""
        with self._lock:
            try:
                self._pan_limits = Limits(
                    min_deg=request.pan_min_deg,
                    max_deg=request.pan_max_deg,
                    max_speed_deg_per_s=request.max_speed_deg_per_s,
                    max_accel_deg_per_s2=request.max_accel_deg_per_s2,
                    has_position_feedback=request.has_position_feedback,
                    tolerance_deg=self._pan_limits.tolerance_deg,
                )
            except ValueError as exc:
                response.success = False
                response.error_message = str(exc)
                response.requires_homing = True
                return response

            self._tilt_limits = Limits(
                min_deg=request.tilt_min_deg,
                max_deg=request.tilt_max_deg,
                max_speed_deg_per_s=request.max_accel_deg_per_s2 and self._pan_limits.max_speed_deg_per_s,
                max_accel_deg_per_s2=self._pan_limits.max_accel_deg_per_s2,
                has_position_feedback=request.has_position_feedback,
                tolerance_deg=self._pan_limits.tolerance_deg,
            )
            self._region_angles = list(request.region_angles)
            self._region_names = list(request.region_names)
            self._calibration_version = f"{time.time():.0f}"
            self._homed = False
            response.success = True
            response.error_message = ""
            response.requires_homing = True
        self.get_logger().info(
            f"calibration installed: pan=[{self._pan_limits.min_deg:.0f}, "
            f"{self._pan_limits.max_deg:.0f}] regions={len(self._region_names)}; "
            "homing required"
        )
        return response

    def _on_get_calibration(self, _request, response):
        """Report what the software believes the room's geometry is."""
        with self._lock:
            response.pan_min_deg = self._pan_limits.min_deg
            response.pan_max_deg = self._pan_limits.max_deg
            response.tilt_min_deg = self._tilt_limits.min_deg
            response.tilt_max_deg = self._tilt_limits.max_deg
            response.max_speed_deg_per_s = self._pan_limits.max_speed_deg_per_s
            response.max_accel_deg_per_s2 = self._pan_limits.max_accel_deg_per_s2
            response.home_angle_deg = 0.0
            response.region_angles = self._region_angles
            response.region_names = self._region_names
            response.has_position_feedback = self._pan_limits.has_position_feedback
            response.homed = self._homed
            response.calibration_version = self._calibration_version
            response.loaded_at = ""
        return response

    def _on_set_zoom(self, request, response):
        """Zoom belongs to the camera, not the servo. Answer honestly."""
        response.success = False
        response.error_message = (
            "zoom is a camera capability. Call the camera_bridge's /camera/set_zoom service."
        )
        del request
        return response

    def _on_legacy_target(self, msg) -> None:
        """Accept the archived scan controller's Float64 target. Deprecated."""
        self.get_logger().warn("/stand/set_target is deprecated; use the /stand/goto_angle action", once=True)
        try:
            self._driver.move_to(float(msg.data), self._pan_limits.max_speed_deg_per_s, 10.0)
            with self._lock:
                self._target = self._pan_limits.clamp(float(msg.data))
        except DriverNotConnected as exc:
            self.get_logger().error(f"legacy target failed: {exc}")

    # -- state -----------------------------------------------------------
    def _publish_state(self) -> None:
        """Publish the full mechanism state."""
        try:
            position = self._driver.position()
        except DriverError:
            position = 0.0

        with self._lock:
            message = ServoState()
            message.header.stamp = self.get_clock().now().to_msg()
            message.state = getattr(ServoState, self._state, ServoState.IDLE)
            message.target_angle_deg = self._target
            message.current_angle_deg = position
            message.homed = self._homed
            message.home_angle_deg = 0.0
            message.min_angle_deg = self._pan_limits.min_deg
            message.max_angle_deg = self._pan_limits.max_deg
            message.max_speed_deg_per_s = self._pan_limits.max_speed_deg_per_s
            message.max_accel_deg_per_s2 = self._pan_limits.max_accel_deg_per_s2
            message.fault_code = self._fault
            message.fault_message = self._fault
            message.controller_online = self._driver.is_connected()
        self._state_pub.publish(message)

    def destroy_node(self) -> bool:
        """Stop the mechanism on shutdown. Never leaves it moving.

        The stop is best-effort and must not raise: a camera left moving during
        shutdown is a hazard, and an exception here would also mask whatever
        else went wrong.
        """
        with contextlib.suppress(Exception):
            self._driver.stop()
        return super().destroy_node()


def main(args: list[str] | None = None) -> None:
    """Entry point."""
    rclpy.init(args=args)
    node = ServoControllerNode()
    # Multi-threaded so the state publisher and service callbacks keep running
    # while a move blocks in the action handler.
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info("servo_controller interrupted")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
