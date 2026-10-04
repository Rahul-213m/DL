#!/usr/bin/env python3
"""edge_uploader node: drains the outbox to the cloud when it can.

Runs on a timer, on its own thread, entirely independently of the scan. The
scan path calls ``enqueue`` and returns; nothing about a sweep depends on this
node succeeding, and nothing here depends on the scan still running.

Uses urllib rather than an HTTP client library, for the same reason
``camera_bridge`` does: this runs on a stock ROS image, and a missing
dependency in the field is a field failure.

Three behaviours worth naming:

* **Idempotency key on content hash**, so a retry after a timeout that
  actually succeeded does not create a duplicate attendance row.
* **Give up after N attempts.** An image the server consistently rejects will
  not start working, and a poison item at the head of the queue blocks
  everything behind it.
* **Reports queue depth**, so an operator can see a build-up before it becomes
  lost data.
"""

from __future__ import annotations

import json
import threading
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

import rclpy
from rclpy.node import Node

from edge_uploader.outbox import EdgeOutbox, QueuedCapture
from edge_uploader.transport import build_frame_request, read_device_secret

SECONDS_PER_HOUR = 3600.0


class EdgeUploaderNode(Node):
    """Drains the durable outbox to the cloud."""

    def __init__(self) -> None:
        super().__init__("edge_uploader")
        self.declare_parameter("data_root", "/var/lib/attendance")
        self.declare_parameter("base_url", "https://attendance.example.com")
        self.declare_parameter("cloud_session_id", 0)
        self.declare_parameter("device_secret_file", "/etc/attendance/device-secret")
        self.declare_parameter("tenant_id", "00000000-0000-0000-0000-000000000000")
        self.declare_parameter("device_id", "unprovisioned")
        self.declare_parameter("batch_size", 10)
        self.declare_parameter("max_attempts", 5)
        self.declare_parameter("upload_interval_s", 30.0)
        self.declare_parameter("request_timeout_s", 30.0)
        self.declare_parameter("min_faces_to_upload", 1)

        self._tenant = str(self.get_parameter("tenant_id").value)
        self._device = str(self.get_parameter("device_id").value)
        self._base_url = str(self.get_parameter("base_url").value).rstrip("/")
        self._request_timeout = float(self.get_parameter("request_timeout_s").value)
        self._max_attempts = int(self.get_parameter("max_attempts").value)
        self._batch = int(self.get_parameter("batch_size").value)
        try:
            self._device_secret = read_device_secret(
                Path(str(self.get_parameter("device_secret_file").value))
            )
        except (OSError, ValueError) as exc:
            self._device_secret = ""
            self.get_logger().error(f"device uploads disabled: {exc}")

        self._outbox = EdgeOutbox(
            root=str(self.get_parameter("data_root").value),
            tenant_id=self._tenant,
            device_id=self._device,
            min_faces_to_upload=int(self.get_parameter("min_faces_to_upload").value),
        )
        self._lock = threading.Lock()
        self._uploading = False
        self._last_error = ""
        self._uploaded_total = 0
        self._last_run = 0.0

        self._timer = self.create_timer(float(self.get_parameter("upload_interval_s").value), self._tick)

        stats = self._outbox.stats()
        self.get_logger().info(
            f"outbox ready at {self.get_parameter('data_root').value}: "
            f"{stats['pending']} pending, {stats['total_bytes'] / 1_000_000:.1f} MB of "
            f"{stats['max_bytes'] / 1_000_000:.0f} MB"
        )
        if self._tenant == "00000000-0000-0000-0000-000000000000":
            # A null tenant is better than no tenant: the server rejects it,
            # rather than filing one classroom's faces under another school.
            self.get_logger().error(
                "tenant_id is UNPROVISIONED. Uploads will be rejected by the server. "
                "This is deliberate: it is far better to upload nothing than to file a "
                "classroom's biometric data under the wrong tenant."
            )

    # -- main loop ------------------------------------------------------
    def _tick(self) -> None:
        """Drain whatever is pending. Safe to call when already running."""
        with self._lock:
            if self._uploading:
                return
            self._uploading = True
        try:
            self._drain()
        except Exception as exc:  # noqa: BLE001 - a timer must never die
            self._last_error = f"{type(exc).__name__}: {exc}"
            self.get_logger().error(f"upload cycle failed: {self._last_error}")
        finally:
            with self._lock:
                self._uploading = False
            self._last_run = time.monotonic()

    def _drain(self) -> None:
        """Upload one batch."""
        session_id = int(self.get_parameter("cloud_session_id").value)
        if not self._device_secret:
            self._last_error = "device secret is not provisioned"
            return
        if session_id <= 0:
            self._last_error = "cloud_session_id is not set to an open cloud session"
            return
        batch = self._outbox.next_batch(self._batch)
        if not batch:
            return
        self.get_logger().info(f"uploading {len(batch)} capture(s)")
        for capture in batch:
            self._upload_one(capture, session_id)

    def _upload_one(self, capture: QueuedCapture, session_id: int) -> None:
        """Upload a single capture, recording the outcome either way."""
        try:
            image = capture.image_path.read_bytes()
            if not image:
                raise OSError("queued capture is empty")
            request = build_frame_request(
                base_url=self._base_url,
                session_id=session_id,
                device_id=capture.device_id,
                device_secret=self._device_secret,
                frame_id=capture.capture_id,
                device_timestamp=capture.captured_at,
                correlation_id=uuid.uuid4().hex,
                camera_angle_deg=capture.camera_angle_deg,
                zoom=capture.zoom,
                image=image,
            )
            with urllib.request.urlopen(request, timeout=self._request_timeout) as response:
                body = json.loads(response.read().decode() or "{}")
        except urllib.error.HTTPError as exc:
            # 4xx will not fix itself. 5xx might. Do not conflate them.
            retryable = exc.code >= 500
            self._outbox.mark_failed(
                capture.capture_id,
                f"HTTP {exc.code}",
                max_attempts=self._max_attempts if retryable else 1,
            )
            return
        except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            self._outbox.mark_failed(
                capture.capture_id, f"{type(exc).__name__}: {exc}", max_attempts=self._max_attempts
            )
            return

        self._outbox.mark_uploaded(capture.capture_id, body.get("frame_id", capture.capture_id))
        self._uploaded_total += 1
        self._last_error = ""
        self.get_logger().info(f"uploaded {capture.capture_id[:8]} ({capture.size_bytes / 1000:.0f} kB)")

    # -- status ---------------------------------------------------------
    def stats(self) -> dict:
        """Current queue state, for the operator console and for tests."""
        stats = self._outbox.stats()
        stats["uploaded_total"] = self._uploaded_total
        stats["last_error"] = self._last_error
        stats["tenant_id"] = self._tenant
        return stats


def main(args: list[str] | None = None) -> None:
    """Entry point."""
    rclpy.init(args=args)
    node = EdgeUploaderNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
