#!/usr/bin/env python3
"""
camera_interface.py
===================
Simulated Camera Interface Node for the Attendance Camera Stand.

RESPONSIBILITY
--------------
This node provides a clean ROS 2 service interface for "capture an
image now".  In the real system this node would be replaced by (or
communicate with) a phone app that:
  1. Receives the capture request over Wi-Fi/MQTT.
  2. Triggers the phone camera.
  3. Saves or streams the image.
  4. Returns success/failure.

The rest of the system (scan_controller) uses the same ROS 2 service
interface regardless of whether a real or simulated camera is used.

SERVICES (provided)
-------------------
  /camera/capture   [std_srvs/Trigger]
      Request an image capture.
      - success: True  if capture simulated/performed successfully.
      - message: status message including angle and timestamp.

TOPICS (published)
------------------
  /camera/status    [std_msgs/String]
      Human-readable status: "IDLE" | "CAPTURING" | "ERROR"

  /camera/capture_count  [std_msgs/Int32]
      Total number of captures performed in this session.

TOPICS (subscribed)
-------------------
  /stand/current_angle  [std_msgs/Float64]
      The camera interface subscribes to the current angle so it can
      include the angle in its log and response message.

PARAMETERS (declared, loaded from scan.yaml)
--------------------------------------------
  capture_delay   [float, seconds]   default 0.5
      Simulated shutter delay before the service returns.

FUTURE PHONE INTEGRATION
------------------------
To integrate a real phone camera:
  Option A — Replace this node entirely:
    The phone app (e.g. a ROS 2 Android/iOS node) advertises the same
    /camera/capture service.  No changes needed in scan_controller.

  Option B — Bridge approach:
    Keep this node but replace the _simulate_capture() method with a
    call to the phone over MQTT/HTTP/WebSocket.  The service interface
    remains identical to the rest of the ROS 2 system.

  The captured images should be published on:
    /camera/image_raw  [sensor_msgs/Image]
  or saved to a configurable directory for the AI attendance system
  to process separately (the AI processing is NOT this node's job).
"""

import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32, Float64
from std_srvs.srv import Trigger


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

class CameraInterfaceNode(Node):
    """Simulated camera interface for the attendance camera stand."""

    STATUS_IDLE      = "IDLE"
    STATUS_CAPTURING = "CAPTURING"
    STATUS_ERROR     = "ERROR"

    def __init__(self):
        super().__init__('camera_interface')

        # ---- Declare parameters -----------------------------------------------
        self.declare_parameter('capture_delay', 0.5)   # seconds

        self._capture_delay = self.get_parameter('capture_delay').value

        self.get_logger().info(
            f'CameraInterface starting: capture_delay={self._capture_delay}s'
        )

        # ---- Internal state ---------------------------------------------------
        self._status:         str   = self.STATUS_IDLE
        self._capture_count:  int   = 0
        self._current_angle:  float = 0.0   # updated by subscription

        # ---- Subscribers ------------------------------------------------------
        self._sub_angle = self.create_subscription(
            Float64,
            '/stand/current_angle',
            self._on_angle_update,
            10
        )

        # ---- Publishers -------------------------------------------------------
        self._pub_status = self.create_publisher(
            String, '/camera/status', 10)

        self._pub_count = self.create_publisher(
            Int32, '/camera/capture_count', 10)

        # ---- Services ---------------------------------------------------------
        self._srv_capture = self.create_service(
            Trigger, '/camera/capture', self._on_capture_request)

        # ---- Timer (status publisher) -----------------------------------------
        self._timer = self.create_timer(0.5, self._publish_status)

        self.get_logger().info('CameraInterface ready. Waiting for capture requests.')

    # -------------------------------------------------------------------------
    # Subscription callbacks
    # -------------------------------------------------------------------------

    def _on_angle_update(self, msg: Float64):
        """Keep track of current stand angle for logging purposes."""
        self._current_angle = msg.data

    # -------------------------------------------------------------------------
    # Service callback
    # -------------------------------------------------------------------------

    def _on_capture_request(self, request, response):
        """
        Handle a camera capture request from scan_controller.

        In simulation: log the capture event and return success.
        In production: trigger the phone camera, receive image, return result.
        """
        self._status = self.STATUS_CAPTURING
        self._publish_status()

        self.get_logger().info(
            '╔═══════════════════════════════════════╗'
        )
        self.get_logger().info(
            '║     CAMERA CAPTURE REQUEST RECEIVED   ║'
        )
        self.get_logger().info(
            f'║  Angle     : {self._current_angle:>6.1f} degrees          ║'
        )
        self.get_logger().info(
            f'║  Capture # : {self._capture_count + 1:<6d}                 ║'
        )
        self.get_logger().info(
            f'║  Timestamp : {self.get_clock().now().to_msg().sec:<20d} ║'
        )
        self.get_logger().info(
            '╚═══════════════════════════════════════╝'
        )

        # Simulate shutter delay
        if self._capture_delay > 0.0:
            # NOTE: time.sleep() is acceptable here because this node is
            # single-threaded and the service client (scan_controller) is
            # already waiting for the response.
            time.sleep(self._capture_delay)

        # In the real system:
        #   - Send capture command to phone
        #   - Wait for image acknowledgment
        #   - Optionally save image path for the AI system
        success = self._simulate_capture()

        if success:
            self._capture_count += 1
            self._status = self.STATUS_IDLE
            response.success = True
            response.message = (
                f'Capture #{self._capture_count} at {self._current_angle:.1f}° OK'
            )
            self.get_logger().info(
                f'Capture #{self._capture_count} completed at '
                f'{self._current_angle:.1f}°.'
            )
        else:
            self._status = self.STATUS_ERROR
            response.success = False
            response.message = 'Capture FAILED (simulated error)'
            self.get_logger().error('Capture FAILED.')

        self._publish_count()
        return response

    # -------------------------------------------------------------------------
    # Simulation helper
    # -------------------------------------------------------------------------

    def _simulate_capture(self) -> bool:
        """
        Placeholder for a real capture operation.

        Returns True to simulate a successful capture.

        FUTURE REPLACEMENT:
          This method should be replaced with actual phone camera
          communication, e.g.:
            result = self._phone_client.call_async(CaptureRequest())
            return result.success
        """
        # Simulated camera always succeeds
        return True

    # -------------------------------------------------------------------------
    # Publishers
    # -------------------------------------------------------------------------

    def _publish_status(self):
        msg = String()
        msg.data = self._status
        self._pub_status.publish(msg)

    def _publish_count(self):
        msg = Int32()
        msg.data = self._capture_count
        self._pub_count.publish(msg)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(args=None):
    rclpy.init(args=args)
    node = CameraInterfaceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info(
            f'CameraInterface shutting down. '
            f'Total captures this session: {node._capture_count}'
        )
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
