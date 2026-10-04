"""HTTP transport for the cloud frame-ingestion endpoint."""

from __future__ import annotations

import json
import secrets
import stat
import urllib.request
from pathlib import Path


def read_device_secret(path: Path) -> str:
    """Read a provisioned secret from a regular file inaccessible to other users."""
    file_stat = path.stat()
    if not stat.S_ISREG(file_stat.st_mode):
        raise ValueError("device secret path must be a regular file")
    if stat.S_IMODE(file_stat.st_mode) & 0o077:
        raise ValueError("device secret file permissions must be 0600")
    secret = path.read_text(encoding="utf-8").strip()
    if len(secret) < 32:
        raise ValueError("device secret must contain at least 32 characters")
    return secret


def build_frame_request(
    *,
    base_url: str,
    session_id: int,
    device_id: str,
    device_secret: str,
    frame_id: str,
    device_timestamp: str,
    correlation_id: str,
    camera_angle_deg: float | None,
    zoom: float | None,
    image: bytes,
) -> urllib.request.Request:
    """Build the multipart request expected by ``POST /v1/sessions/{id}/frames``."""
    boundary = f"attendance-{secrets.token_hex(16)}"
    metadata = json.dumps(
        {
            "frame_id": frame_id,
            "device_timestamp": device_timestamp,
            "correlation_id": correlation_id,
            "camera_angle_deg": camera_angle_deg,
            "zoom": zoom,
        },
        separators=(",", ":"),
    ).encode("utf-8")
    body = b"".join(
        (
            f"--{boundary}\r\n".encode(),
            b'Content-Disposition: form-data; name="meta"\r\n',
            b"Content-Type: application/json\r\n\r\n",
            metadata,
            b"\r\n",
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="content"; filename="{frame_id}.jpg"\r\n'.encode(),
            b"Content-Type: image/jpeg\r\n\r\n",
            image,
            b"\r\n",
            f"--{boundary}--\r\n".encode(),
        )
    )
    return urllib.request.Request(
        f"{base_url.rstrip('/')}/v1/sessions/{session_id}/frames",
        data=body,
        method="POST",
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "X-Device-Id": device_id,
            "X-Device-Secret": device_secret,
            "X-Correlation-Id": correlation_id,
        },
    )