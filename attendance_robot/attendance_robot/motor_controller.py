#!/usr/bin/env python3
"""
motor_controller.py
===================
Simulated Motor Controller Node for the Attendance Camera Stand.

RESPONSIBILITY
--------------
This node simulates a rotating stand motor.  It maintains the
target and current angular position of the stand and publishes
them on ROS 2 topics.

In the real system this node (or an equivalent) would forward
commands over Wi-Fi / Bluetooth to an ESP32, which would drive
a servo or stepper motor.  The rest of the system (scan_controller)
communicates with this node via the same topics and services,
so swapping in the real hardware requires ONLY changing this file.

TOPICS (published)
------------------
  /stand/current_angle  [std_msgs/Float64]
      Current angle of the stand in degrees (0-359.9, normalised).

  /stand/target_angle   [std_msgs/Float64]
      Target angle that the motor is moving toward (degrees).

  /stand/status         [std_msgs/String]
      Human-readable status string.
      Values: "IDLE" | "MOVING" | "AT_TARGET" | "ERROR"

TOPICS (subscribed)
-------------------
  /stand/set_target     [std_msgs/Float64]
      Send a new target angle (degrees).  Normalised automatically.

SERVICES
--------
  /stand/stop           [std_srvs/Trigger]
      Stop motion immediately; hold current angle as new target.

  /stand/reset          [std_srvs/Trigger]
      Reset stand to 0 degrees.

PARAMETERS (declared, loaded from scan.yaml)
--------------------------------------------
  rotation_speed   [float, deg/s]  default 45.0
  publish_rate     [float, Hz]     default 10.0

FUTURE ESP32 INTEGRATION
------------------------
Replace the _simulate_motion() logic with:
  1. Publish the target angle to an MQTT/serial topic forwarded to ESP32.
  2. Read the encoder feedback from ESP32 and update self._current_angle.
  3. Keep all topic/service interfaces identical.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64, String
from std_srvs.srv import Trigger


# ---------------------------------------------------------------------------
# Utility functions (also imported by unit tests)
# ---------------------------------------------------------------------------

def normalise_angle(degrees: float) -> float:
    """Return angle normalised to [0, 360)."""
    return degrees % 360.0


def angle_difference(current: float, target: float) -> float:
    """
    Shortest signed angular difference from current to target (degrees).
    Result is in the range (-180, 180].
    Positive = need to rotate forward (CCW).
    Negative = need to rotate backward (CW).
    """
    diff = (target - current) % 360.0
    if diff > 180.0:
        diff -= 360.0
    return diff


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

class MotorControllerNode(Node):
    """Simulated motor controller for the attendance camera stand."""

    STATUS_IDLE      = "IDLE"
    STATUS_MOVING    = "MOVING"
    STATUS_AT_TARGET = "AT_TARGET"
    STATUS_ERROR     = "ERROR"

    def __init__(self):
        super().__init__('motor_controller')

        # ---- Declare parameters -----------------------------------------------
        self.declare_parameter('rotation_speed', 45.0)   # deg/s
        self.declare_parameter('publish_rate',   10.0)   # Hz

        self._rotation_speed = float(self.get_parameter('rotation_speed').value)
        self._publish_rate   = float(self.get_parameter('publish_rate').value)

        self.get_logger().info(
            f'MotorController starting: '
            f'speed={self._rotation_speed} deg/s, '
            f'publish_rate={self._publish_rate} Hz'
        )

        # ---- Internal state ---------------------------------------------------
        self._current_angle: float = 0.0   # degrees, normalised 0-360
        self._target_angle:  float = 0.0   # degrees, normalised 0-360
        self._status:        str   = self.STATUS_IDLE
        self._stopped:       bool  = False  # emergency stop flag

        # Snap threshold: snap to target when this close (deg).
        # Set to half a timer tick of travel to prevent overshoot jitter.
        # At 45 deg/s and 10 Hz, one tick = 4.5 deg; use 0.5 deg for safety.
        self._snap_threshold: float = 0.5

        # ---- Publishers -------------------------------------------------------
        self._pub_current = self.create_publisher(
            Float64, '/stand/current_angle', 10)

        self._pub_target = self.create_publisher(
            Float64, '/stand/target_angle', 10)

        self._pub_status = self.create_publisher(
            String, '/stand/status', 10)

        # ---- Subscriptions ----------------------------------------------------
        self._sub_set_target = self.create_subscription(
            Float64,
            '/stand/set_target',
            self._on_set_target,
            10
        )

        # ---- Services ---------------------------------------------------------
        self._srv_stop = self.create_service(
            Trigger, '/stand/stop', self._on_stop)

        self._srv_reset = self.create_service(
            Trigger, '/stand/reset', self._on_reset)

        # ---- Simulation timer ------------------------------------------------
        period = 1.0 / self._publish_rate
        self._timer = self.create_timer(period, self._timer_callback)

        self.get_logger().info('MotorController ready.')

    # -------------------------------------------------------------------------
    # Subscription callbacks
    # -------------------------------------------------------------------------

    def _on_set_target(self, msg: Float64):
        """Receive a new target angle from scan_controller."""
        raw_angle = msg.data
        new_target = normalise_angle(raw_angle)

        self._stopped = False
        self._target_angle = new_target

        # Only switch to MOVING if we are not already there
        diff = angle_difference(self._current_angle, self._target_angle)
        if abs(diff) > self._snap_threshold:
            self._status = self.STATUS_MOVING
        else:
            # Already at target (e.g. moving to 0 when already at 0)
            self._current_angle = self._target_angle
            self._status = self.STATUS_AT_TARGET

        self.get_logger().info(
            f'New target: {new_target:.1f} deg  '
            f'(current: {self._current_angle:.1f} deg, '
            f'diff: {diff:+.1f} deg)'
        )

    # -------------------------------------------------------------------------
    # Service callbacks
    # -------------------------------------------------------------------------

    def _on_stop(self, request, response):
        """Stop the motor immediately; hold current position."""
        self._stopped = True
        self._target_angle = self._current_angle
        self._status = self.STATUS_IDLE
        response.success = True
        response.message = f'Motor stopped at {self._current_angle:.1f} deg'
        self.get_logger().warn(
            f'STOP command received. Holding at {self._current_angle:.1f} deg')
        return response

    def _on_reset(self, request, response):
        """Reset the stand to 0 degrees."""
        self._stopped = False
        self._target_angle = 0.0
        self._status = self.STATUS_MOVING
        response.success = True
        response.message = 'Resetting to 0 deg'
        self.get_logger().info('Reset command received. Moving to 0 deg.')
        return response

    # -------------------------------------------------------------------------
    # Simulation timer callback
    # -------------------------------------------------------------------------

    def _timer_callback(self):
        """
        Advance the simulated motor one time-step and publish state.

        In a real system this would:
          1. Read encoder position from ESP32.
          2. Compare with target; send velocity/step command to ESP32.
          3. Publish the real encoder position (replacing self._current_angle).
        """
        dt = 1.0 / self._publish_rate  # seconds per tick

        if not self._stopped:
            self._simulate_motion(dt)

        # Publish current angle
        current_msg = Float64()
        current_msg.data = self._current_angle
        self._pub_current.publish(current_msg)

        # Publish target angle
        target_msg = Float64()
        target_msg.data = self._target_angle
        self._pub_target.publish(target_msg)

        # Publish status
        status_msg = String()
        status_msg.data = self._status
        self._pub_status.publish(status_msg)

    def _simulate_motion(self, dt: float):
        """
        Move current_angle one step toward target_angle.

        Uses shortest-path rotation:
          e.g. 350 deg -> 10 deg rotates +20 deg (not -340 deg).
        """
        diff = angle_difference(self._current_angle, self._target_angle)

        if abs(diff) <= self._snap_threshold:
            # Snap to exact target to avoid floating-point drift
            self._current_angle = self._target_angle
            if self._status == self.STATUS_MOVING:
                self._status = self.STATUS_AT_TARGET
                self.get_logger().info(
                    f'Reached target: {self._target_angle:.1f} deg')
            return

        # Move at most one full step toward the target
        max_step = self._rotation_speed * dt
        step = max(-max_step, min(max_step, diff))
        self._current_angle = normalise_angle(self._current_angle + step)
        self._status = self.STATUS_MOVING


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node = MotorControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('MotorController shutting down.')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
