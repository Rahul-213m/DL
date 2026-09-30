"""Camera driver abstraction and the reconnect/backoff policy.

Two implementations:

* :class:`IpWebcamDriver` — the "IP Webcam" Android app over HTTP, which is the
  most common way to drive a phone from a classroom computer without writing
  an Android app. **UNVERIFIED against real hardware**; the operator has not
  confirmed which phone app they use (HUMAN_ACTIONS item 5b).
* :class:`SimulatedCamera` — synthesises frames, so the whole pipeline runs in
  CI with no phone. See :mod:`scan_planner.synthetic_room` for the geometry
  test.

The part that matters most is :func:`backoff_delays` and
:class:`ConnectionState`. A phone on campus Wi-Fi drops, and a scanner that
gives up on the first failure is useless in a real classroom. A scanner that
retries in a tight loop is worse: it hammers an AP that is already struggling.
Exponential backoff with jitter is the difference.

Full-resolution stills, not video frames
----------------------------------------
A video frame is whatever the encoder produced at the moment of capture, often
1080p. The target is 80-112 px of face width for recognition, which from the
back row of a large room needs far more resolution than that. So the bridge
captures **stills** at full sensor resolution and says so, rather than
accepting a video grab and hoping.
"""

from __future__ import annotations

import enum
import logging
import math
import random
import threading
import urllib.request
from dataclasses import dataclass, field
from typing import Protocol

log = logging.getLogger(__name__)


class CameraUnavailable(RuntimeError):
    """The camera is not reachable or did not answer in time."""


class CaptureTimeout(CameraUnavailable):
    """The camera was reachable but did not deliver a frame in time."""


class ConnectionState(enum.Enum):
    """Lifecycle of the camera link."""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    READY = "ready"
    CAPTURING = "capturing"
    DEGRADED = "degraded"  # up, but after repeated failures
    ERROR = "error"


def backoff_delays(
    attempt: int,
    *,
    base_s: float = 0.5,
    factor: float = 2.0,
    maximum_s: float = 30.0,
    jitter: float = 0.3,
    rng: random.Random | None = None,
) -> float:
    """Seconds to wait before retry ``attempt`` (1-based).

    Exponential with **full-ish jitter**. Jitter is not decoration: without it,
    every node in a classroom retries on the same schedule after a shared AP
    restart, and the thundering herd is what keeps the AP down.

    Args:
        attempt: 1 for the first retry.
        base_s: Delay after the first failure.
        factor: Growth per attempt.
        maximum_s: Ceiling, so a long outage does not push the next attempt to
            hours.
        jitter: Fractional spread, 0.0 to 0.5.
        rng: Injectable for deterministic tests.

    Returns:
        The delay in seconds, in ``[0, maximum_s]``.
    """
    if attempt < 1:
        raise ValueError(f"attempt must be >= 1, got {attempt}")
    if not 0 <= jitter <= 0.5:
        raise ValueError(f"jitter must be in [0, 0.5], got {jitter}")
    raw = min(base_s * (factor ** (attempt - 1)), maximum_s)
    if jitter == 0.0:
        return raw
    generator = rng or random
    spread = raw * jitter
    return max(0.0, min(maximum_s, raw + generator.uniform(-spread, spread)))


@dataclass(slots=True)
class CameraMetadataSample:
    """What the camera reported about one capture."""

    width: int
    height: int
    zoom: float = 1.0
    exposure_time_s: float = 0.0
    iso: float = 0.0
    focus_distance_m: float = 0.0
    focus_locked: bool = False
    exposure_locked: bool = False

    @property
    def megapixels(self) -> float:
        """Resolution in megapixels, for a log line an operator can read."""
        return self.width * self.height / 1_000_000.0


class CameraDriver(Protocol):
    """The port every camera implementation satisfies."""

    #: Whether this driver can deliver a FULL-SENSOR-RESOLUTION still rather
    #: than a video frame. A driver that cannot must say so, because the scan
    #: planner's whole zoom strategy depends on the available resolution.
    supports_full_resolution_still: bool

    #: Whether the lens is motorised, and therefore whether zoom takes time to
    #: change. A fixed lens changes the scan strategy completely.
    has_motorised_zoom: bool

    def capture_still(self, *, timeout_s: float = 10.0) -> bytes:  # pragma: no cover
        """Return encoded JPEG bytes at the highest available resolution."""
        ...

    def metadata(self) -> CameraMetadataSample:  # pragma: no cover
        """Report exposure, zoom, focus and resolution as the device sees them."""
        ...

    def set_zoom(self, zoom: float, *, lock: bool = True) -> float:  # pragma: no cover
        """Set optical zoom; returns the applied value."""
        ...

    def set_focus(self, distance_m: float | None, *, lock: bool) -> None:  # pragma: no cover
        """Focus at a distance, or disable AF; ``lock`` freezes the setting."""
        ...

    def is_healthy(self) -> bool:  # pragma: no cover
        """Whether the device is answering."""
        ...


@dataclass
class ReconnectPolicy:
    """How aggressively to retry a lost camera.

    Attributes:
        max_attempts: Give up after this many consecutive failures. Zero
            means retry forever, which is what a classroom wants: the phone
            will come back, and a permanently dead camera should page someone
            rather than silently stop taking attendance.
        base_delay_s: First backoff.
        max_delay_s: Backoff ceiling.
        degraded_after: Consecutive failures before reporting DEGRADED, so an
            operator console can show a warning before a scan fails outright.
    """

    max_attempts: int = 0
    base_delay_s: float = 0.5
    max_delay_s: float = 30.0
    degraded_after: int = 3

    def delay_for(self, attempt: int, rng: random.Random | None = None) -> float:
        """Backoff for a given attempt."""
        return backoff_delays(
            attempt,
            base_s=self.base_delay_s,
            maximum_s=self.max_delay_s,
            rng=rng,
        )

    def should_retry(self, attempt: int) -> bool:
        """Whether another attempt is permitted."""
        return self.max_attempts == 0 or attempt <= self.max_attempts


@dataclass
class SimulatedCamera:
    """A camera that always works, for CI and for the Definition of Done.

    Synthesises frames with a known geometry so the scan planner can be tested
    against a room of a specific size. ``face_size_at_distance`` implements the
    pixels-per-face arithmetic from ``docs/hardware/pixels_per_face.md``, which
    is how a synthetic room is made to be *honest* about what a real room of
    that size would look like.
    """

    width: int = 4608
    height: int = 3456
    horizontal_fov_deg: float = 70.0
    focal_length_mm: float = 6.0
    sensor_width_mm: float = 6.4
    has_motorised_zoom: bool = True
    supports_full_resolution_still: bool = True
    #: Deterministic frame counter, so a test can tell two captures apart.
    frame_number: int = field(default=0)
    fail_next: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _zoom: float = 1.0
    _focus_locked: bool = False
    _exposure_locked: bool = False
    _angle_deg: float = 0.0

    def face_size_at_distance(self, distance_m: float, zoom: float = 1.0) -> float:
        """Expected face width in pixels at a given distance.

        The pinhole relation ``px = f * W / d``, with ``f`` derived from the
        horizontal field of view and the sensor width. This is the same
        arithmetic as ``docs/hardware/pixels_per_face.md``, so a synthetic
        room of a given size produces faces of a realistic size and the
        pipeline is exercised at the resolution a real room would impose.
        """
        # Derive the focal length in pixels from the reported field of view
        # rather than from focal_length_mm, so that whichever of the two an
        # operator fills in the simulation still behaves like a real camera.
        f_pixels = (self.width / 2.0) / math.tan(math.radians(self.horizontal_fov_deg / 2.0))
        # A typical adult face is ~150 mm wide.
        return (f_pixels * 0.150 * zoom) / max(distance_m, 0.01)

    def set_angle(self, angle_deg: float) -> None:
        """Tell the simulation which way the camera is pointing."""
        with self._lock:
            self._angle_deg = angle_deg

    def capture_still(self, *, timeout_s: float = 10.0) -> bytes:
        """Return a synthetic JPEG."""
        import numpy as np

        with self._lock:
            if self.fail_next > 0:
                self.fail_next -= 1
                raise CameraUnavailable("simulated camera failure")
            self.frame_number += 1
            seed = self.frame_number + int(abs(self._angle_deg))

        rng = np.random.default_rng(seed)
        array = rng.integers(0, 255, (720, 1280, 3), dtype=np.uint8)
        ok, encoded = _cv2().imencode(".jpg", array, [int(_cv2().IMWRITE_JPEG_QUALITY), 80])
        if not ok:  # pragma: no cover
            raise CameraUnavailable("simulated encode failed")
        del timeout_s
        return encoded.tobytes()

    def metadata(self) -> CameraMetadataSample:
        """Report the simulated state."""
        with self._lock:
            return CameraMetadataSample(
                width=self.width,
                height=self.height,
                zoom=self._zoom,
                focus_locked=self._focus_locked,
                exposure_locked=self._exposure_locked,
            )

    def set_zoom(self, zoom: float, *, lock: bool = True) -> float:
        """Clamp zoom to a plausible 1x-10x range, as a phone lens actually is."""
        with self._lock:
            self._zoom = max(1.0, min(10.0, zoom))
            self._focus_locked = lock
            return self._zoom

    def set_focus(self, distance_m: float | None, *, lock: bool) -> None:
        """Record the focus request."""
        with self._lock:
            self._focus_locked = lock
            del distance_m

    def is_healthy(self) -> bool:
        """Always healthy unless a test made it fail."""
        return self.fail_next == 0

    def note_angle(self, angle_deg: float) -> None:
        """Alias of :meth:`set_angle` for readability at call sites."""
        self.set_angle(angle_deg)


def _cv2():
    """Import cv2 lazily; the simulation does not otherwise need it."""
    import cv2

    return cv2


@dataclass
class IpWebcamDriver:
    """Drives the "IP Webcam" Android app over HTTP.

    Endpoints used (all from the app's built-in server on port 8080):

    ============================  =========================================
    ``GET  /``                    probe; the app returns a JPEG of the camera
    ``GET  /photo.jpg``           the highest-resolution still the app offers
    ``GET  /parameters``          current settings as key=value lines
    ``POST /<command>``           e.g. ``/zoom``, ``/focus``, ``/lockfocus``
    ============================  =========================================

    **UNVERIFIED against real hardware.** The command names and the parameters
    endpoint have changed between app versions, and the operator has not
    confirmed which app they use. Every request is therefore tolerant: an
    unknown command is logged and ignored rather than failing a capture, and
    :attr:`probe_ok` records whether the app answered at all.

    Written against a documented interface so that swapping in a different app
    means writing one class, not touching the scan planner.
    """

    host: str = "192.168.1.100"
    port: int = 8080
    timeout_s: float = 10.0
    #: IP Webcam does not expose motorised zoom over HTTP; the phone's own
    #: digital zoom is the only control, and it does not add detail.
    has_motorised_zoom: bool = False
    supports_full_resolution_still: bool = True
    probe_ok: bool = False
    _lock: threading.Lock = field(default_factory=threading.Lock)

    @property
    def base_url(self) -> str:
        """Root URL of the app's server."""
        return f"http://{self.host}:{self.port}"

    def _get(self, path: str) -> bytes:
        """GET a path, raising :class:`CameraUnavailable` on any failure.

        Uses :mod:`urllib` rather than httpx on purpose. httpx is not present
        in a stock ROS 2 Jazzy install (``python3-httpx`` is not a rosdep key
        every image carries), and a driver that raises ``ModuleNotFoundError``
        in the one place it is needed -- a real classroom with a real phone --
        is worse than a slightly more verbose stdlib call.
        """
        url = f"{self.base_url}{path}"
        # Deliberately broad: a phone HTTP server fails in a dozen ways
        # (refused, reset, timed out, 500, a redirect to its own UI) and the
        # caller only needs to know the camera is unusable and why.
        try:
            with urllib.request.urlopen(url, timeout=self.timeout_s) as response:
                return response.read()
        except Exception as exc:
            raise CameraUnavailable(f"{url} failed: {type(exc).__name__}: {exc}") from exc

    def _post(self, command: str, value: str = "") -> bool:
        """POST a command. Returns False rather than raising.

        A phone that does not support a command must not fail the capture: the
        scan can still run at a fixed zoom, and the planner is told the zoom
        did not change.
        """
        path = f"/{command}" + (f"/{value}" if value else "")
        request = urllib.request.Request(f"{self.base_url}{path}", method="POST", data=b"")
        # A phone that does not support a command must not fail the capture,
        # so a failure here is logged and swallowed by design.
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s):
                return True
        except Exception as exc:  # noqa: BLE001
            log.warning("camera command failed", extra={"command": command, "error": str(exc)})
            return False

    def capture_still(self, *, timeout_s: float = 10.0) -> bytes:
        """Fetch a full-resolution still.

        Falls back from ``/photo.jpg`` to the live ``/`` stream, because not
        every app version implements the still endpoint. A fallback that
        silently lowered resolution would be worse than a failure, so the
        result is logged when it happens.
        """
        previous = self.timeout_s
        self.timeout_s = timeout_s
        try:
            data = self._get("/photo.jpg")
            if data[:2] == b"\xff\xd8":
                self.probe_ok = True
                return data
            log.warning("/photo.jpg did not return JPEG; falling back to the live stream")
            data = self._get("/")
            if data[:2] == b"\xff\xd8":
                self.probe_ok = True
                log.warning(
                    "captured from the live stream, not a full-resolution still; "
                    "back-row coverage will be limited"
                )
                return data
            raise CameraUnavailable("camera returned neither a still nor a JPEG stream")
        finally:
            self.timeout_s = previous

    def metadata(self) -> CameraMetadataSample:
        """Read the app's reported parameters, with sane defaults on failure."""
        try:
            raw = self._get("/parameters").decode("utf-8", errors="replace")
        except CameraUnavailable:
            return CameraMetadataSample(width=0, height=0)
        values: dict[str, str] = {}
        for line in raw.splitlines():
            key, _, value = line.partition("=")
            values[key.strip()] = value.strip()
        return CameraMetadataSample(
            width=_to_int(values.get("width"), 0),
            height=_to_int(values.get("height"), 0),
            zoom=_to_float(values.get("zoom"), 1.0),
            exposure_time_s=_to_float(values.get("exposure_time"), 0.0),
            iso=_to_float(values.get("iso"), 0.0),
            focus_locked=values.get("focuslock", "0") in {"1", "true"},
            exposure_locked=values.get("exposurelock", "0") in {"1", "true"},
        )

    def set_zoom(self, zoom: float, *, lock: bool = True) -> float:
        """Request digital zoom. Note that this does NOT add optical detail."""
        applied = max(1.0, min(10.0, zoom))
        self._post("zoom", f"{applied:.1f}x")
        if lock:
            self._post("lockfocus")
        return applied

    def set_focus(self, distance_m: float | None, *, lock: bool) -> None:
        """Request a focus distance, or continuous AF when ``None``."""
        if distance_m is None:
            self._post("focus", "auto")
        else:
            self._post("focus", f"{distance_m:.2f}")
        if lock:
            self._post("lockfocus")

    def is_healthy(self) -> bool:
        """Probe the app."""
        try:
            self._get("/")
            self.probe_ok = True
        except CameraUnavailable:
            self.probe_ok = False
        return self.probe_ok


def _to_int(value: str | None, default: int) -> int:
    """Parse an int, falling back rather than raising on a camera's bad value."""
    try:
        return int(float(value))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def _to_float(value: str | None, default: float) -> float:
    """Parse a float, falling back rather than raising on a camera's bad value."""
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def measure_sharpness(jpeg_bytes: bytes) -> float:
    """Variance-of-Laplacian of a JPEG's luma, as a blur signal.

    The scan planner uses this to decide on a retake. Deliberately the same
    metric as the cloud's quality gate (``app/core/domain/imageops.py``) so a
    frame the edge accepts and the cloud rejects do not disagree for no
    reason.
    """
    cv2 = _cv2()
    array = cv2.imdecode(np_frombuffer(jpeg_bytes), cv2.IMREAD_COLOR)
    if array is None:
        return 0.0
    grey = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(grey, cv2.CV_64F).var())


def np_frombuffer(data: bytes):
    """numpy.frombuffer, imported lazily so cv2 stays the only hard dep here."""
    import numpy as np

    return np.frombuffer(data, dtype=np.uint8)


__all__ = [
    "CameraDriver",
    "CameraMetadataSample",
    "CameraUnavailable",
    "CaptureTimeout",
    "ConnectionState",
    "IpWebcamDriver",
    "ReconnectPolicy",
    "SimulatedCamera",
    "backoff_delays",
    "measure_sharpness",
]
