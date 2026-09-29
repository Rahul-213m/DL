#!/usr/bin/env python3
"""
scan_controller.py
==================
Main Orchestration Node for the Attendance Camera Stand.

RESPONSIBILITY
--------------
This is the "brain" of the system.  It:
  1. Loads scan angles from the config file (scan.yaml).
  2. Commands the motor controller to rotate to each angle.
  3. Waits until the stand reaches the target angle.
  4. Waits an additional stabilization period (prevents motion blur).
  5. Calls the camera capture service.
  6. Advances to the next angle.
  7. After the last angle, returns to 0 degrees.
  8. Optionally repeats for N cycles.

SCAN SEQUENCE (per cycle)
-------------------------
  For each angle in scan_angles:
    1. Publish angle  ->  /stand/set_target
    2. Wait until     <-  /stand/current_angle is within angle_tolerance
    3. Sleep          :   stabilization_time seconds  (prevents blur)
    4. Call service   ->  /camera/capture
    5. Wait for       <-  service response
  After final angle:
    6. Publish 0.0    ->  /stand/set_target  (return home)
    7. Wait for motor to reach 0

IMPLEMENTATION NOTE
-------------------
The scan loop runs in a background thread so the ROS 2 service callbacks
(/scan/start, /scan/stop) can return immediately.

We use MultiThreadedExecutor so that:
  - The main executor thread keeps processing subscriptions and publishing
    status updates while the scan thread sleeps.
  - The camera /camera/capture service call_async() future gets resolved
    by the executor (required -- a future dispatched via call_async only
    completes when the executor calls spin_once).

TOPICS (subscribed)
-------------------
  /stand/current_angle  [std_msgs/Float64]   Motor current position
  /stand/status         [std_msgs/String]    Motor status string

TOPICS (published)
------------------
  /stand/set_target     [std_msgs/Float64]   Commanded angle

  /scan/status          [std_msgs/String]    Scan session status
      Values: "IDLE" | "SCANNING" | "STABILIZING" | "CAPTURING" |
              "RETURNING" | "COMPLETE" | "STOPPED" | "ERROR"

  /scan/current_index   [std_msgs/Int32]     Index into scan_angles list

SERVICES (provided)
-------------------
  /scan/start           [std_srvs/Trigger]   Start (or restart) a scan session.
  /scan/stop            [std_srvs/Trigger]   Abort the current scan session.

SERVICES (used)
---------------
  /camera/capture       [std_srvs/Trigger]   Request image capture.

PARAMETERS (declared, loaded from scan.yaml)
--------------------------------------------
  scan_angles          [list[int]]  angles to visit in degrees
  stabilization_time   [float]      seconds to wait after reaching angle
  number_of_cycles     [int]        0 = infinite, >0 = fixed count
  angle_tolerance      [float]      degrees -- "close enough" threshold
  motor_timeout        [float]      seconds before giving up waiting
"""

import threading
import time
from typing import Optional

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import Float64, String, Int32
from std_srvs.srv import Trigger


# ---------------------------------------------------------------------------
# Utility functions (also used by unit tests)
# ---------------------------------------------------------------------------

def normalise_angle(degrees: float) -> float:
    """Return angle normalised to [0, 360)."""
    return degrees % 360.0


def angle_close_enough(current: float, target: float, tolerance: float) -> bool:
    """
    Return True if current is within tolerance of target using shortest-path
    angular difference (handles 0/360 wrap-around).
    """
    diff = abs(((current - target) + 180.0) % 360.0 - 180.0)
    return diff <= tolerance


# ---------------------------------------------------------------------------
# Scan state constants
# ---------------------------------------------------------------------------

class ScanState:
    IDLE        = "IDLE"
    SCANNING    = "SCANNING"
    STABILIZING = "STABILIZING"
    CAPTURING   = "CAPTURING"
    RETURNING   = "RETURNING"
    COMPLETE    = "COMPLETE"
    STOPPED     = "STOPPED"
    ERROR       = "ERROR"


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

class ScanControllerNode(Node):
    """Main orchestration node for the attendance camera stand."""

    def __init__(self):
        super().__init__('scan_controller')

        # ---- Declare parameters -----------------------------------------------
        self.declare_parameter('scan_angles',        [0, 60, 120, 180, 240, 300])
        self.declare_parameter('stabilization_time', 1.0)
        self.declare_parameter('number_of_cycles',   1)
        self.declare_parameter('angle_tolerance',    1.0)
        self.declare_parameter('motor_timeout',      10.0)

        self._scan_angles        = list(self.get_parameter('scan_angles').value)
        self._stabilization_time = float(self.get_parameter('stabilization_time').value)
        self._number_of_cycles   = int(self.get_parameter('number_of_cycles').value)
        self._angle_tolerance    = float(self.get_parameter('angle_tolerance').value)
        self._motor_timeout      = float(self.get_parameter('motor_timeout').value)

        # Normalise all configured angles once at startup
        self._scan_angles = [normalise_angle(float(a)) for a in self._scan_angles]

        self.get_logger().info(
            f'ScanController starting:\n'
            f'  scan_angles      = {self._scan_angles}\n'
            f'  stabilization    = {self._stabilization_time}s\n'
            f'  cycles           = '
            f'{"inf" if self._number_of_cycles == 0 else self._number_of_cycles}\n'
            f'  angle_tolerance  = {self._angle_tolerance} deg\n'
            f'  motor_timeout    = {self._motor_timeout}s'
        )

        # ---- Internal state ---------------------------------------------------
        self._state: str              = ScanState.IDLE
        self._current_motor_angle: float = 0.0
        self._motor_status: str       = "IDLE"
        self._current_scan_index: int = 0
        self._completed_cycles: int   = 0
        self._stop_requested: bool    = False

        # Guards concurrent start calls
        self._scan_lock = threading.Lock()
        # Scan runs in a daemon thread so it doesn't block process exit
        self._scan_thread: Optional[threading.Thread] = None

        # ---- Subscriptions ----------------------------------------------------
        self._sub_angle = self.create_subscription(
            Float64, '/stand/current_angle', self._on_angle_update, 10)

        self._sub_motor_status = self.create_subscription(
            String, '/stand/status', self._on_motor_status, 10)

        # ---- Publishers -------------------------------------------------------
        self._pub_set_target = self.create_publisher(
            Float64, '/stand/set_target', 10)

        self._pub_scan_status = self.create_publisher(
            String, '/scan/status', 10)

        self._pub_scan_index = self.create_publisher(
            Int32, '/scan/current_index', 10)

        # ---- Services (provided) -----------------------------------------------
        self._srv_start = self.create_service(
            Trigger, '/scan/start', self._on_start)

        self._srv_stop = self.create_service(
            Trigger, '/scan/stop', self._on_stop)

        # ---- Service client (camera) -------------------------------------------
        # The client is created here; the actual call happens in the scan thread.
        # Because we use MultiThreadedExecutor the future will be resolved by
        # the executor even while the scan thread is blocked polling for it.
        self._cli_capture = self.create_client(Trigger, '/camera/capture')

        # ---- Status publisher timer -------------------------------------------
        self._status_timer = self.create_timer(0.5, self._publish_status)

        self.get_logger().info(
            'ScanController ready.\n'
            '  Start scan : ros2 service call /scan/start std_srvs/srv/Trigger\n'
            '  Stop scan  : ros2 service call /scan/stop  std_srvs/srv/Trigger'
        )

    # -------------------------------------------------------------------------
    # Subscription callbacks (called from the executor)
    # -------------------------------------------------------------------------

    def _on_angle_update(self, msg: Float64):
        self._current_motor_angle = msg.data

    def _on_motor_status(self, msg: String):
        self._motor_status = msg.data

    # -------------------------------------------------------------------------
    # Service callbacks (provided)
    # -------------------------------------------------------------------------

    def _on_start(self, request, response):
        """Start a new scan session."""
        with self._scan_lock:
            if self._scan_thread is not None and self._scan_thread.is_alive():
                if self._state not in (ScanState.COMPLETE, ScanState.STOPPED,
                                       ScanState.IDLE, ScanState.ERROR):
                    response.success = False
                    response.message = (
                        f'Scan already in progress (state={self._state}). '
                        f'Call /scan/stop first.'
                    )
                    return response

            self._stop_requested = False
            self._completed_cycles = 0
            self._current_scan_index = 0
            self._state = ScanState.SCANNING

            self._scan_thread = threading.Thread(
                target=self._run_scan_loop, daemon=True, name='scan_loop')
            self._scan_thread.start()

        response.success = True
        response.message = (
            f'Scan started: {len(self._scan_angles)} angles, '
            f'{"inf" if self._number_of_cycles == 0 else self._number_of_cycles} '
            f'cycle(s). stabilization={self._stabilization_time}s.'
        )
        self.get_logger().info('=== SCAN SESSION STARTED ===')
        return response

    def _on_stop(self, request, response):
        """Abort the current scan session."""
        self._stop_requested = True
        # State will be set to STOPPED by the scan loop itself
        response.success = True
        response.message = 'Stop requested. Scan will halt after current step.'
        self.get_logger().warn('=== SCAN STOP REQUESTED ===')
        return response

    # -------------------------------------------------------------------------
    # Status publisher (called by timer, every 0.5s)
    # -------------------------------------------------------------------------

    def _publish_status(self):
        msg = String()
        msg.data = self._state
        self._pub_scan_status.publish(msg)

        idx_msg = Int32()
        idx_msg.data = self._current_scan_index
        self._pub_scan_index.publish(idx_msg)

    # -------------------------------------------------------------------------
    # Scan loop (runs in background thread)
    # -------------------------------------------------------------------------

    def _run_scan_loop(self):
        """
        Execute the configured number of scan cycles.
        Each cycle: visit every angle, capture, then return to 0.
        """
        try:
            cycle = 0
            while rclpy.ok() and not self._stop_requested:
                cycle += 1
                if self._number_of_cycles > 0 and cycle > self._number_of_cycles:
                    break

                label = (
                    f'inf' if self._number_of_cycles == 0
                    else str(self._number_of_cycles)
                )
                self.get_logger().info(
                    f'--- Starting cycle {cycle} / {label} ---'
                )

                if not self._execute_cycle(cycle):
                    self.get_logger().warn(f'Cycle {cycle} aborted early.')
                    break

                self._completed_cycles = cycle

            # --- Return home ---
            if not self._stop_requested:
                self.get_logger().info(
                    f'All {self._completed_cycles} cycle(s) complete. '
                    f'Returning to 0 deg...'
                )
                self._state = ScanState.RETURNING
                self._send_target(0.0)
                self._wait_for_target(0.0)
                self._state = ScanState.COMPLETE
                self.get_logger().info(
                    f'=== SCAN SESSION COMPLETE '
                    f'({self._completed_cycles} cycle(s)) ==='
                )
            else:
                self._state = ScanState.STOPPED
                self.get_logger().info('Scan stopped by request.')

        except Exception as exc:
            self._state = ScanState.ERROR
            self.get_logger().error(f'Scan loop exception: {exc}')

    def _execute_cycle(self, cycle_number: int) -> bool:
        """
        Visit each scan angle in order:
          MOVE -> REACH TARGET -> STABILIZE -> CAPTURE -> next angle
        Returns True if cycle completed normally, False if aborted.
        """
        for idx, angle in enumerate(self._scan_angles):
            if self._stop_requested:
                return False

            self._current_scan_index = idx

            self.get_logger().info(
                f'[Cycle {cycle_number}] '
                f'Step {idx + 1}/{len(self._scan_angles)}: '
                f'Moving to {angle:.0f} deg'
            )

            # ---- 1. Command motor -------------------------------------------
            self._state = ScanState.SCANNING
            self._send_target(angle)

            # ---- 2. Wait for motor to reach target --------------------------
            reached = self._wait_for_target(angle)
            if not reached:
                self.get_logger().warn(
                    f'Motor timeout waiting for {angle:.0f} deg. '
                    f'Continuing with capture anyway.'
                )

            if self._stop_requested:
                return False

            # ---- 3. Stabilization wait  -------------------------------------
            # Stand is at the target angle. Wait before capturing so any
            # residual vibration / motion settles.
            self.get_logger().info(
                f'  At {angle:.0f} deg. '
                f'Stabilizing for {self._stabilization_time}s...'
            )
            self._state = ScanState.STABILIZING
            # Use small sleep increments so stop requests are detected quickly
            self._interruptible_sleep(self._stabilization_time)

            if self._stop_requested:
                return False

            # ---- 4. Camera capture ------------------------------------------
            self._state = ScanState.CAPTURING
            self.get_logger().info(
                f'  Stabilization complete. '
                f'Requesting capture at {angle:.0f} deg...'
            )
            capture_ok = self._call_capture()

            if capture_ok:
                self.get_logger().info(
                    f'  Capture OK at {angle:.0f} deg.'
                )
            else:
                self.get_logger().error(
                    f'  Capture FAILED at {angle:.0f} deg.'
                )
                # Log the failure but continue to next angle

        return True

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _send_target(self, angle: float):
        """Publish a normalised target angle to the motor controller."""
        angle = normalise_angle(angle)
        msg = Float64()
        msg.data = angle
        self._pub_set_target.publish(msg)

    def _wait_for_target(self, target_angle: float) -> bool:
        """
        Block the scan thread until:
          - /stand/current_angle is within angle_tolerance of target, OR
          - motor_timeout seconds elapse.
        Returns True if target reached, False on timeout.
        Polls at 10 Hz using 0.1s sleeps so the thread stays responsive.
        """
        target_angle = normalise_angle(target_angle)
        deadline = time.monotonic() + self._motor_timeout

        while time.monotonic() < deadline:
            if self._stop_requested:
                return False

            if angle_close_enough(
                    self._current_motor_angle, target_angle,
                    self._angle_tolerance):
                return True

            time.sleep(0.1)

        return False  # timed out

    def _interruptible_sleep(self, duration: float):
        """Sleep for `duration` seconds, waking every 0.1s to check stop flag."""
        end = time.monotonic() + duration
        while time.monotonic() < end:
            if self._stop_requested:
                return
            time.sleep(min(0.1, end - time.monotonic()))

    def _call_capture(self) -> bool:
        """
        Call /camera/capture synchronously from the scan background thread.

        Uses call_async() + polling.  The future is resolved by the
        MultiThreadedExecutor running on the main thread -- this is why
        MultiThreadedExecutor is required (a SingleThreadedExecutor would
        deadlock here because spin() is already blocking the main thread).

        Returns True on success, False on error/timeout.
        """
        if not self._cli_capture.wait_for_service(timeout_sec=3.0):
            self.get_logger().error('/camera/capture service not available!')
            return False

        future = self._cli_capture.call_async(Trigger.Request())

        # Poll until the executor resolves the future
        deadline = time.monotonic() + 10.0
        while not future.done():
            if time.monotonic() > deadline:
                self.get_logger().error('Camera capture call timed out (10s).')
                return False
            time.sleep(0.05)

        result = future.result()
        if result is None:
            self.get_logger().error('Camera capture returned None result.')
            return False

        return bool(result.success)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node = ScanControllerNode()
    # MultiThreadedExecutor is required so that:
    #   - The scan background thread's call_async() futures are resolved.
    #   - Subscription callbacks keep delivering angle/status updates
    #     while the scan thread is sleeping.
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info('ScanController shutting down.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
