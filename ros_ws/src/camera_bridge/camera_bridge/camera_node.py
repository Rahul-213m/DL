#!/usr/bin/env python3
"""camera_bridge node.

Wraps a phone camera behind a ROS interface: full-resolution stills, zoom and
focus control, reconnect with backoff, and a heartbeat.

Replaces the legacy ``camera_interface`` node, whose ``_simulate_capture()``
was ``return True`` — it never produced an image, so nothing downstream could
have worked against it.

What this adds over a direct call:

* **Reconnect with exponential backoff and jitter.** A phone on campus Wi-Fi
  drops. A tight retry loop makes an already-struggling AP worse.
* **A heartbeat**, so an operator console can tell "the camera is fine and the
  room is dark" from "the camera is gone".
* **A DEGRADED state** after repeated failures, so a warning appears before a
  scan fails outright.
* **A capture counter and a failure counter**, because "is it working?" is the
  first question anyone asks and the answer should not require a log search.
"""

from __future__ import annotations

import threading
import time

import rclpy
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

from attendance_interfaces.msg import CaptureStatus
from attendance_interfaces.srv import CaptureStill, SetZoom
from camera_bridge.driver import (
    CameraUnavailable,
    ConnectionState,
    IpWebcamDriver,
    ReconnectPolicy,
    SimulatedCamera,
    measure_sharpness,
)

FAULT_TIMEOUT = "capture_timeout"
FAULT_UNAVAILABLE = "camera_unavailable"


class CameraBridgeNode(Node):
    """Still capture with zoom control, reconnect and a heartbeat."""

    def __init__(self) -> None:
        super().__init__("camera_bridge")
        self.declare_parameter("driver", "simulated")
        self.declare_parameter("ip_webcam_host", "192.168.1.100")
        self.declare_parameter("ip_webcam_port", 8080)
        self.declare_parameter("capture_timeout_s", 10.0)
        self.declare_parameter("heartbeat_hz", 1.0)
        self.declare_parameter("max_reconnect_attempts", 0)
        self.declare_parameter("reconnect_base_delay_s", 0.5)
        self.declare_parameter("reconnect_max_delay_s", 30.0)
        self.declare_parameter("degraded_after_failures", 3)
        self.declare_parameter("min_sharpness", 0.0)
        self.declare_parameter("lock_focus", True)
        self.declare_parameter("lock_exposure", True)
        self.declare_parameter("default_zoom", 1.0)

        driver_name = str(self.get_parameter("driver").value)
        if driver_name == "simulated":
            self._camera = SimulatedCamera()
        elif driver_name == "ip_webcam":
            self._camera = IpWebcamDriver(
                host=str(self.get_parameter("ip_webcam_host").value),
                port=int(self.get_parameter("ip_webcam_port").value),
            )
        else:
            raise ValueError(f"unknown driver '{driver_name}'; use 'simulated' or 'ip_webcam'")

        self._policy = ReconnectPolicy(
            max_attempts=int(self.get_parameter("max_reconnect_attempts").value),
            base_delay_s=float(self.get_parameter("reconnect_base_delay_s").value),
            max_delay_s=float(self.get_parameter("reconnect_max_delay_s").value),
            degraded_after=int(self.get_parameter("degraded_after_failures").value),
        )
        self._min_sharpness = float(self.get_parameter("min_sharpness").value)
        self._state = ConnectionState.DISCONNECTED
        self._consecutive_failures = 0
        self._capture_count = 0
        self._detail = ""
        self._retry_at = 0.0
        self._last_capture = 0.0
        self._lock = threading.RLock()
        self._current_zoom = float(self.get_parameter("default_zoom").value)

        callbacks = ReentrantCallbackGroup()
        self._status_pub = self.create_publisher(
            CaptureStatus, "/camera/status", 10, callback_group=callbacks
        )
        self._timer = self.create_timer(
            1.0 / max(float(self.get_parameter("heartbeat_hz").value), 0.1),
            self._publish_status,
            callback_group=callbacks,
        )
        self.create_service(CaptureStill, "/camera/capture", self._on_capture, callback_group=callbacks)
        self.create_service(SetZoom, "/camera/set_zoom", self._on_set_zoom, callback_group=callbacks)

        self.get_logger().info(
            f"CameraBridge ready: driver={driver_name} "
            f"full_res_still={self._camera.supports_full_resolution_still} "
            f"motorised_zoom={self._camera.has_motorised_zoom}"
        )
        if not self._camera.has_motorised_zoom:
            self.get_logger().warn(
                "this camera has NO motorised optical zoom. Digital zoom does not add "
                "detail, so the scan planner's 'zoom pass' cannot work as designed and "
                "back-row coverage will be limited. See docs/hardware/pixels_per_face.md."
            )

    # -- capture ---------------------------------------------------------
    def _on_capture(self, request, response):
        """Capture one still, with retries and an honest failure result."""
        with self._lock:
            self._state = ConnectionState.CAPTURING
        started = time.monotonic()
        timeout = (
            float(request.timeout_s)
            if request.timeout_s > 0
            else float(self.get_parameter("capture_timeout_s").value)
        )

        attempt = 0
        last_error = ""
        while True:
            attempt += 1
            try:
                data = self._camera.capture_still(timeout_s=timeout)
            except CameraUnavailable as exc:
                last_error = str(exc)
                if not self._policy.should_retry(attempt):
                    break
                delay = self._policy.delay_for(attempt)
                self.get_logger().warn(f"capture failed ({last_error}); retry {attempt} in {delay:.1f}s")
                with self._lock:
                    self._retry_at = time.monotonic() + delay
                    self._consecutive_failures = attempt
                    self._state = (
                        ConnectionState.CONNECTING
                        if attempt < self._policy.degraded_after
                        else ConnectionState.DEGRADED
                    )
                    self._detail = last_error
                time.sleep(delay)
                continue

            # A slow capture is its own failure: the phone may have taken the
            # shot but a phone that needs 30s is unusable for a sweep.
            elapsed = time.monotonic() - started
            if elapsed > timeout:
                last_error = f"capture took {elapsed:.1f}s, over the {timeout:.1f}s budget"
                break

            sharpness = measure_sharpness(data)
            metadata = self._camera.metadata()
            with self._lock:
                self._state = ConnectionState.READY
                self._consecutive_failures = 0
                self._capture_count += 1
                self._last_capture = time.monotonic()
                self._detail = ""

            response.success = True
            response.error_code = ""
            response.error_message = ""
            response.queued_for_upload = True
            response.captured_at = self.get_clock().now().to_msg()
            response.sha256 = _sha256(data)
            response.size_bytes = len(data)
            response.queued_for_upload = True
            response.metadata = _metadata_message(self, metadata, sharpness)
            self.get_logger().info(
                f"captured #{self._capture_count} "
                f"{metadata.width}x{metadata.height} "
                f"zoom={metadata.zoom:.1f} sharpness={sharpness:.0f} "
                f"in {elapsed:.2f}s"
            )
            return response

        with self._lock:
            self._state = ConnectionState.ERROR
            self._detail = last_error
        response.success = False
        response.error_code = FAULT_TIMEOUT if "over the" in last_error else FAULT_UNAVAILABLE
        response.error_message = last_error
        response.queued_for_upload = False
        self.get_logger().error(f"capture failed after {attempt} attempt(s): {last_error}")
        return response

    def _on_set_zoom(self, request, response):
        """Change zoom, reporting the value actually applied."""
        with self._lock:
            self._current_zoom = float(request.zoom)
        applied = self._camera.set_zoom(float(request.zoom), lock=bool(request.lock))
        # IP Webcam applies DIGITAL zoom, which interpolates pixels and adds no
        # detail. Say so, because a scan planner that believes it gained
        # resolution will plan badly.
        if not self._camera.has_motorised_zoom and applied > 1.0:
            response.success = True
            response.error_message = (
                "applied, but this is DIGITAL zoom: it interpolates and adds no detail. "
                "Back-row coverage will not improve. See docs/hardware/pixels_per_face.md."
            )
            self.get_logger().warn(f"digital zoom to {applied:.1f}x requested: no additional detail")
        else:
            response.success = True
            response.error_message = ""
        response.applied_zoom = applied
        response.settle_time_s = 0.5 if self._camera.has_motorised_zoom else 0.0
        return response

    # -- status ----------------------------------------------------------
    def _publish_status(self) -> None:
        """Publish the heartbeat."""
        message = CaptureStatus()
        with self._lock:
            message.state = {
                ConnectionState.DISCONNECTED: CaptureStatus.UNAVAILABLE,
                ConnectionState.CONNECTING: CaptureStatus.CONNECTING,
                ConnectionState.READY: CaptureStatus.READY,
                ConnectionState.CAPTURING: CaptureStatus.CAPTURING,
                ConnectionState.DEGRADED: CaptureStatus.DEGRADED,
                ConnectionState.ERROR: CaptureStatus.ERROR,
            }[self._state]
            message.detail = self._detail
            message.capture_count = self._capture_count
            message.consecutive_failures = self._consecutive_failures
            message.retry_in_s = max(0.0, self._retry_at - time.monotonic())
        # CaptureStatus carries no Header, so the timestamp is a plain field.
        message.last_capture_at = (
            self.get_clock().now().to_msg() if self._last_capture > 0.0 else _zero_time()
        )
        message.heartbeat_hz = float(self.get_parameter("heartbeat_hz").value)
        self._status_pub.publish(message)


def _zero_time():
    """A ROS time meaning 'never', since there is no optional."""
    from builtin_interfaces.msg import Time

    return Time()


def _metadata_message(node, metadata, sharpness: float):
    """Build a CameraMetadata message from a driver sample."""
    from attendance_interfaces.msg import CameraMetadata

    message = CameraMetadata()
    message.header.stamp = node.get_clock().now().to_msg()
    message.captured_at = node.get_clock().now().to_msg()
    message.zoom = float(metadata.zoom)
    message.exposure_time_s = float(metadata.exposure_time_s)
    message.iso = float(metadata.iso)
    message.focus_distance_m = float(metadata.focus_distance_m)
    message.focus_locked = bool(metadata.focus_locked)
    message.exposure_locked = bool(metadata.exposure_locked)
    message.width = int(metadata.width)
    message.height = int(metadata.height)
    message.channel_order = "BGR"
    message.exif_orientation = 1
    # The camera's own angle, when it can report one. A phone has no encoder,
    # so this is the last pan angle the bridge was told, and the flag says so
    # rather than presenting it as a measurement.
    message.has_camera_angle = False
    message.camera_angle_deg = 0.0
    message.extra_keys = ["sharpness"]
    message.extra_values = [f"{sharpness:.2f}"]
    del node._min_sharpness
    return message


def _sha256(data: bytes) -> str:
    """SHA-256 of an image, so a corrupted upload is detectable."""
    import hashlib

    return hashlib.sha256(data).hexdigest()


def main(args: list[str] | None = None) -> None:
    """Entry point."""
    rclpy.init(args=args)
    node = CameraBridgeNode()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info("camera_bridge interrupted")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
