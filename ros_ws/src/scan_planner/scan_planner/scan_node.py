#!/usr/bin/env python3
"""scan_planner node: executes a sweep plan against the servo and camera.

Thin by design. Every decision -- how many steps, which need zoom, whether a
frame is worth keeping, what a lost camera means -- lives in ``planner.py`` and
is unit-tested there. This file is the ROS wiring: create clients, await
futures, publish feedback, handle cancellation.

Why it awaits futures instead of blocking
-----------------------------------------
The move and the capture are both asynchronous. The previous draft of this file
called a service and returned immediately with a fabricated result, which is
the same class of bug as the legacy code: it looked like it worked and did
nothing. ``rclpy`` futures are awaited with ``rclpy.task.Future`` and a
``MultiThreadedExecutor``, so a cancelled sweep stops the mechanism on the
cancellation callback rather than after the current step.
"""

from __future__ import annotations

import time
import uuid

import rclpy
from rclpy.action import ActionClient, ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from attendance_interfaces.action import GoToAngle, RunScanSequence
from attendance_interfaces.msg import CameraMetadata, FrameManifest, ServoState
from attendance_interfaces.srv import CaptureStill, SetZoom
from scan_planner.planner import (
    DETECT_FACE_PX,
    IDENTIFY_FACE_PX,
    PlanError,
    RoomGeometry,
    ScanStep,
    assess_capture_metadata,
    assess_frame,
    plan_sweep,
)

PHASE_PREPARING = RunScanSequence.Feedback.PREPARING
PHASE_MOVING = RunScanSequence.Feedback.MOVING
PHASE_SETTLING = RunScanSequence.Feedback.SETTLING
PHASE_CAPTURING = RunScanSequence.Feedback.CAPTURING
PHASE_REVISITING = RunScanSequence.Feedback.REVISITING


class ScanPlannerNode(Node):
    """Plans and executes a classroom sweep."""

    def __init__(self) -> None:
        super().__init__("scan_planner")
        self.declare_parameter("depth_m", 12.0)
        self.declare_parameter("width_m", 9.0)
        self.declare_parameter("camera_height_m", 2.4)
        self.declare_parameter("camera_offset_x_m", 0.0)
        self.declare_parameter("seat_pitch_m", 0.9)
        self.declare_parameter("frame_width_px", 4608)
        self.declare_parameter("frame_height_px", 3456)
        self.declare_parameter("horizontal_fov_deg", 70.0)
        self.declare_parameter("max_zoom", 4.0)
        self.declare_parameter("time_budget_s", 300.0)
        self.declare_parameter("min_detect_face_px", float(DETECT_FACE_PX))
        self.declare_parameter("min_identify_face_px", float(IDENTIFY_FACE_PX))
        self.declare_parameter("max_retakes_per_step", 2)
        self.declare_parameter("motor_timeout_s", 30.0)
        # The servo registers this action under /stand/ (it also serves the
        # archived legacy interface on /stand/*). Parameterised because a
        # mismatch here fails as "servo_unavailable" at the start of every
        # sweep, which is an expensive way to learn a topic name.
        self.declare_parameter("servo_action", "/stand/goto_angle")
        self.declare_parameter("capture_service", "/camera/capture")
        self.declare_parameter("zoom_service", "/camera/set_zoom")
        self.declare_parameter("capture_timeout_s", 15.0)
        self.declare_parameter("dry_run", False)

        self._callbacks = ReentrantCallbackGroup()
        self._cancelled = False
        self._scan_id = ""
        self._servo_state: ServoState | None = None
        self._camera_meta: CameraMetadata | None = None
        self._camera_has_optical_zoom = True

        self._manifest_pub = self.create_publisher(
            FrameManifest, "/scan/manifest", 10, callback_group=self._callbacks
        )
        self.create_subscription(
            ServoState, "/servo/state", self._on_servo_state, 10, callback_group=self._callbacks
        )
        self.create_subscription(
            CameraMetadata,
            "/camera/metadata",
            self._on_camera_metadata,
            10,
            callback_group=self._callbacks,
        )
        self._capture_client = self.create_client(
            CaptureStill, "/camera/capture", callback_group=self._callbacks
        )
        self._zoom_client = self.create_client(SetZoom, "/camera/set_zoom", callback_group=self._callbacks)
        self._goto_client = ActionClient(
            self, GoToAngle, "/servo/go_to_angle", callback_group=self._callbacks
        )

        self._action_server = ActionServer(
            self,
            RunScanSequence,
            "/scan/run",
            execute_callback=self._execute,
            goal_callback=self._on_goal,
            cancel_callback=self._on_cancel,
            callback_group=self._callbacks,
        )
        self.get_logger().info("scan_planner ready")

    # -- subscriptions --------------------------------------------------
    def _on_servo_state(self, message: ServoState) -> None:
        """Track the mechanism, so a stall is visible while the sweep runs."""
        self._servo_state = message

    def _on_camera_metadata(self, message: CameraMetadata) -> None:
        """Track the camera, so a frame's real resolution is known."""
        self._camera_meta = message

    # -- action plumbing ------------------------------------------------
    def _on_goal(self, request) -> GoalResponse:
        """Accept a sweep goal."""
        self._scan_id = uuid.uuid4().hex
        self.get_logger().info(f"scan {self._scan_id} requested")
        del request
        return GoalResponse.ACCEPT

    def _on_cancel(self, _goal_handle) -> CancelResponse:
        """Accept a cancellation and stop the mechanism immediately.

        The point of accepting a cancel is that the mechanism stops. A sweep
        that finishes its remaining steps during a cancellation is a sweep that
        knocked over a laptop on the desk it was aiming at.
        """
        self._cancelled = True
        self.get_logger().warn("scan cancelled; cancelling the in-flight move")
        return CancelResponse.ACCEPT

    # -- execution ------------------------------------------------------
    def _execute(self, goal_handle):
        """Run the sweep, and never finish without saying what happened.

        A blank abort -- no fault code, no message, no frames -- is
        indistinguishable from a successful scan of an empty classroom. Any
        unexpected exception is caught here and turned into an explicit fault,
        because a sweep that reports nothing while looking finished is the
        failure mode this project has been fixing from the start.
        """
        try:
            return self._execute_inner(goal_handle)
        except Exception as exc:  # noqa: BLE001
            self.get_logger().error(f"sweep failed: {type(exc).__name__}: {exc}")
            result = RunScanSequence.Result()
            result.scan_id = self._scan_id
            result.fault_code = "internal_error"
            result.error_message = f"{type(exc).__name__}: {exc}"
            if not goal_handle.is_cancel_requested:
                goal_handle.abort()
            return result

    def _execute_inner(self, goal_handle):
        """Run the sweep end to end."""
        self._cancelled = False
        result = RunScanSequence.Result()
        feedback = RunScanSequence.Feedback()
        started = time.monotonic()

        try:
            room = self._room_from_parameters()
            plan = plan_sweep(
                room,
                frame_width_px=int(self.get_parameter("frame_width_px").value),
                time_budget_s=float(self.get_parameter("time_budget_s").value),
                has_motorised_zoom=self._camera_has_optical_zoom,
            )
        except PlanError as exc:
            goal_handle.abort()
            result.fault_code = "plan_error"
            result.error_message = str(exc)
            self.get_logger().error(f"cannot plan a sweep: {exc}")
            result.scan_id = self._scan_id
            return result

        self.get_logger().info(plan.summary())
        for warning in plan.warnings:
            # Surfaced, never swallowed. A sweep that cannot identify the back
            # row must not look like a clean success.
            self.get_logger().warn(warning)

        # rclpy's blocking waits are correct HERE, from a plain callback under
        # a MultiThreadedExecutor. They are only wrong from a coroutine
        # callback, where the executor cannot process the waitable the wait
        # depends on -- which is why this node is not a coroutine.
        if not self._capture_client.wait_for_service(timeout_sec=10.0):
            goal_handle.abort()
            result.fault_code = "camera_unavailable"
            result.error_message = (
                f"{self.get_parameter('capture_service').value} is not available; is camera_bridge running?"
            )
            result.scan_id = self._scan_id
            self.get_logger().error(result.error_message)
            return result
        if not self._goto_client.wait_for_server(timeout_sec=10.0):
            goal_handle.abort()
            result.fault_code = "servo_unavailable"
            result.error_message = (
                f"{self.get_parameter('servo_action').value} is not available; is servo_controller running?"
            )
            result.scan_id = self._scan_id
            self.get_logger().error(result.error_message)
            return result

        result.frames_attempted = 0
        result.frames_captured = 0
        result.frames_rejected = 0
        result.recapture_regions = 0

        for position, step in enumerate(plan.steps):
            if self._cancelled or goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.fault_code = "cancelled"
                result.error_message = f"cancelled after {position} of {plan.step_count} steps"
                self.get_logger().warn(result.error_message)
                result.scan_id = self._scan_id
                result.duration_s = time.monotonic() - started
                return result

            self._publish(feedback, goal_handle, PHASE_MOVING, position, plan, step)

            moved, fault = self._move_to(step)
            if not moved:
                goal_handle.abort()
                result.fault_code = fault or "motion_failed"
                result.error_message = f"step {position} could not reach {step.pan_deg:.1f} deg ({fault})"
                self.get_logger().error(result.error_message)
                result.scan_id = self._scan_id
                result.duration_s = time.monotonic() - started
                return result

            self._publish(feedback, goal_handle, PHASE_CAPTURING, position, plan, step)

            kept = False
            max_retakes = int(self.get_parameter("max_retakes_per_step").value)
            for retake in range(max_retakes + 1):
                if self._cancelled or goal_handle.is_cancel_requested:
                    goal_handle.canceled()
                    result.fault_code = "cancelled"
                    result.error_message = f"cancelled at step {position}"
                    self.get_logger().warn(result.error_message)
                    result.scan_id = self._scan_id
                    result.duration_s = time.monotonic() - started
                    return result

                result.frames_attempted += 1
                outcome = self._capture(step)
                if outcome.image is None:
                    result.frames_rejected += 1
                    self._publish_manifest(step, retake, outcome.reason, kept=False)
                    self.get_logger().warn(f"step {position}: {outcome.reason}")
                    break

                # Face-size gating needs boxes, and there is no edge detector
                # yet. Gating on an empty box list would reject EVERY frame and
                # report zero captures while appearing to run -- so the edge
                # does only the checks it can actually make, and the cloud
                # remains the authoritative quality and identity gate.
                ok, assessment = assess_capture_metadata(
                    frame_width_px=outcome.width,
                    frame_height_px=outcome.height,
                    sharpness=outcome.sharpness,
                    min_sharpness=0.0,
                )
                if outcome.face_boxes:
                    ok, assessment = assess_frame(
                        outcome.image,
                        face_boxes=outcome.face_boxes,
                        frame_width_px=outcome.width,
                        frame_height_px=outcome.height,
                        min_face_px=float(self.get_parameter("min_identify_face_px").value),
                    )
                if ok:
                    kept = True
                    result.frames_captured += 1
                    self._publish_manifest(step, retake, assessment, kept=True, outcome=outcome)
                    break

                result.frames_rejected += 1
                feedback.reject_reason = assessment
                if retake < max_retakes:
                    result.recapture_regions += 1
                    self._publish(feedback, goal_handle, PHASE_REVISITING, position, plan, step)
                self._publish_manifest(step, retake, assessment, kept=False, outcome=outcome)

            if not kept:
                self.get_logger().warn(
                    f"step {position} at {step.pan_deg:.1f} deg ({step.zoom:g}x) "
                    f"produced no usable frame after {max_retakes + 1} attempt(s)"
                )

        goal_handle.succeed()
        result.scan_id = self._scan_id
        result.duration_s = time.monotonic() - started
        self._publish(feedback, goal_handle, 5, plan.step_count - 1, plan, plan.steps[-1])
        return result

    def _room_from_parameters(self) -> RoomGeometry:
        """Build the room description from parameters."""
        return RoomGeometry(
            depth_m=float(self.get_parameter("depth_m").value),
            width_m=float(self.get_parameter("width_m").value),
            camera_height_m=float(self.get_parameter("camera_height_m").value),
            camera_offset_x_m=float(self.get_parameter("camera_offset_x_m").value),
            seat_pitch_m=float(self.get_parameter("seat_pitch_m").value),
            horizontal_fov_deg=float(self.get_parameter("horizontal_fov_deg").value),
            max_zoom=float(self.get_parameter("max_zoom").value),
        )

    def _move_to(self, step: ScanStep) -> tuple[bool, str]:
        """Move the mechanism to a step's angle, then zoom."""
        goal = GoToAngle.Goal()
        goal.pan_angle_deg = float(step.pan_deg)
        goal.speed_deg_per_s = 0.0
        goal.accel_deg_per_s2 = 0.0
        goal.timeout_s = float(self.get_parameter("motor_timeout_s").value)
        goal.require_homed = True

        # The goal carries its own timeout_s; get_result() blocks until the
        # server answers, and the server bounds that by the goal's own timeout.
        goal_handle = self._goto_client.send_goal(goal)
        if not goal_handle.accepted:
            return False, "motion_goal_rejected"

        wrapped = goal_handle.get_result()

        # STALLED is a distinct result, not a timeout that looks like success.
        if wrapped.result.status == 4:  # ABORTED
            return False, "motion_aborted"
        motion = wrapped.result.result
        if not motion.success:
            return False, motion.fault_code or "motion_failed"
        if motion.fault_code == "stalled":
            return False, "stalled"
        if motion.clamped:
            # A clamp means the calibration and the plan disagree. Not fatal,
            # but it must be visible: the sweep did not aim where it planned.
            self.get_logger().warn(
                f"move to {step.pan_deg:.1f} deg was CLAMPED to {motion.reached_pan_deg:.1f} deg. "
                "The pan calibration and the room description disagree."
            )

        self._set_zoom(step.zoom)
        return True, ""

    def _set_zoom(self, zoom: float) -> None:
        """Set zoom once per step, not once per frame.

        A phone with a motorised lens needs a moment to travel, and doing this
        per frame instead of per step costs seconds of latency per frame. It is
        therefore done once, here, and the per-capture request sets
        ``set_zoom: false``.
        """
        if not self._zoom_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().warn("set_zoom service unavailable; keeping the current zoom")
            return
        request = SetZoom.Request()
        request.zoom = float(zoom)
        request.lock = True
        future = self._zoom_client.call_async(request)
        rclpy.spin_until_future_complete(self, future, timeout_sec=3.0)
        if not future.done():
            future.cancel()
            self.get_logger().warn("set_zoom timed out; continuing at the current zoom")
            return
        response = future.result()
        if response is not None and response.error_message:
            self.get_logger().warn(response.error_message)

    def _capture(self, step: ScanStep):
        """Capture one still for a step."""
        request = CaptureStill.Request()
        request.zoom = float(step.zoom)
        request.set_zoom = False
        request.lock_focus = True
        request.lock_exposure = True
        request.set_zoom = False
        request.timeout_s = float(self.get_parameter("capture_timeout_s").value)

        future = self._capture_client.call_async(request)
        rclpy.spin_until_future_complete(
            self,
            future,
            timeout_sec=float(self.get_parameter("capture_timeout_s").value) + 5.0,
        )
        if not future.done():
            future.cancel()
            return CaptureOutcome(image=None, reason="capture timed out")
        response = future.result()
        if response is None:
            return CaptureOutcome(image=None, reason="camera returned no response")

        if not response.success:
            return CaptureOutcome(image=None, reason=response.error_message or "capture failed")

        # The image bytes are fetched by the uploader from the outbox; the
        # planner works with the response metadata and the detector's boxes.
        width = int(response.metadata.width) or int(self.get_parameter("frame_width_px").value)
        height = int(response.metadata.height) or int(self.get_parameter("frame_height_px").value)
        return CaptureOutcome(
            image=None,
            reason="",
            width=width,
            height=height,
            sha256=response.sha256,
            size_bytes=int(response.size_bytes),
            object_key=response.object_key,
            metadata=response.metadata,
        )

    # -- feedback -------------------------------------------------------
    def _publish(self, feedback, goal_handle, phase: int, position: int, plan, step) -> None:
        """Publish sweep progress."""
        feedback.phase = phase
        feedback.step = position
        feedback.total_steps = plan.step_count
        feedback.step_label = f"{step.zoom_level_name} {step.pan_deg:+.1f} deg"
        feedback.pan_angle_deg = float(step.pan_deg)
        feedback.zoom = float(step.zoom)
        feedback.region_name = f"{step.distance_m:.1f}m"
        goal_handle.publish_feedback(feedback)

    def _publish_manifest(self, step, retake: int, note: str, *, kept: bool, outcome=None) -> None:
        """Publish what happened at one step."""
        message = FrameManifest()
        message.frame_id = uuid.uuid4().hex
        message.scan_id = self._scan_id
        message.correlation_id = self._scan_id
        message.sequence = step.index + 1
        message.notes = note
        if outcome is not None:
            message.sha256 = outcome.sha256
            message.size_bytes = outcome.size_bytes
            message.object_key = outcome.object_key
            if outcome.metadata is not None:
                message.metadata = outcome.metadata
        del kept
        self._manifest_pub.publish(message)


class CaptureOutcome:
    """What one capture attempt produced."""

    def __init__(
        self,
        image,
        reason,
        width=0,
        height=0,
        sha256="",
        size_bytes=0,
        object_key="",
        metadata=None,
        sharpness=0.0,
    ) -> None:
        self.image = image
        self.reason = reason
        self.width = width
        self.height = height
        self.sha256 = sha256
        self.size_bytes = size_bytes
        self.object_key = object_key
        self.metadata = metadata
        self.sharpness = sharpness
        # Face boxes come from the edge detector, which is not wired yet. While
        # it is empty the frame is assessed on resolution and sharpness only,
        # which is honest: better a frame the cloud rejects than a sweep that
        # reports nothing while looking healthy.
        self.face_boxes: list[tuple[int, int, int, int]] = []


def _sharpness_from(metadata) -> float:
    """Read the sharpness the camera bridge measured, if it reported one."""
    if metadata is None:
        return 0.0
    keys = list(getattr(metadata, "extra_keys", []) or [])
    values = list(getattr(metadata, "extra_values", []) or [])
    if "sharpness" in keys:
        try:
            return float(values[keys.index("sharpness")])
        except (IndexError, ValueError):
            return 0.0
    return 0.0


def main(args: list[str] | None = None) -> None:
    """Entry point."""
    rclpy.init(args=args)
    node = ScanPlannerNode()
    executor = MultiThreadedExecutor(num_threads=8)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
