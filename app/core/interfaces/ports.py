"""Ports: the interfaces the domain layer depends on.

Each protocol here is implemented by at least two things — a real adapter and
a fake — so the whole pipeline can be exercised in CI with no hardware, no
model weights and no database. See docs/decisions/0004-hexagonal-ports.md.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np

from app.core.domain.types import BBox, FloatArray

# ---------------------------------------------------------------------------
# Perception
# ---------------------------------------------------------------------------


@runtime_checkable
class Detector(Protocol):
    """Finds faces in an image.

    Contract:
        - Return only faces meeting the configured minimum size and score;
          the caller must not re-filter.
        - ``landmarks`` are five points (left eye, right eye, nose, left mouth,
          right mouth) in source-image pixel coordinates.
        - Must be safe to call concurrently, or the caller must serialise.
    """

    name: str

    def detect(self, image: np.ndarray) -> list[tuple[BBox, np.ndarray, float]]:  # pragma: no cover
        """Return ``[(bbox, landmarks[N,2] float32, score), ...]``."""
        ...

    def warmup(self) -> None:  # pragma: no cover
        """Load weights eagerly so the first real call is not anomalous."""
        ...


@runtime_checkable
class Embedder(Protocol):
    """Turns an aligned face crop into an L2-normalised embedding."""

    name: str
    dimension: int

    def embed(self, aligned_crop: np.ndarray) -> FloatArray:  # pragma: no cover
        """Return a unit-norm embedding of length ``dimension``."""
        ...

    def embed_batch(self, aligned_crops: list[np.ndarray]) -> list[FloatArray]:  # pragma: no cover
        """Embed many crops. May fall back to a loop; batching is an optimisation."""
        ...

    def warmup(self) -> None:  # pragma: no cover
        """Load weights eagerly."""
        ...


@runtime_checkable
class LivenessChecker(Protocol):
    """Optional anti-spoof check.

    Deliberately a separate port. Liveness is a purchase and a policy decision
    (docs/model_licensing.md), and keeping it out of the recogniser means the
    core stays testable without the model.
    """

    name: str

    def check(self, image: np.ndarray, bbox: BBox) -> float:  # pragma: no cover
        """Return a liveness score in ``[0, 1]``; higher is more likely live."""
        ...


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------


@runtime_checkable
class VectorIndex(Protocol):
    """Nearest-neighbour search over L2-normalised embeddings.

    Implementations must be safe to call from multiple threads. The database is
    always the source of truth; this is a rebuildable cache.
    """

    def add(self, entry_id: int, roll_no: str, embedding: FloatArray) -> None:  # pragma: no cover
        """Insert one vector."""
        ...

    def remove(self, entry_id: int) -> None:  # pragma: no cover
        """Delete one vector by its stable id."""
        ...

    def search(self, embedding: FloatArray, k: int) -> list[tuple[str, float, int]]:  # pragma: no cover
        """Return up to ``k`` ``(roll_no, cosine_similarity, entry_id)``, best first."""
        ...

    def rebuild(self) -> int:  # pragma: no cover
        """Reload from the source of truth; returns the resulting size."""
        ...

    @property
    def size(self) -> int:  # pragma: no cover
        """Number of vectors currently indexed."""
        ...


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------


@runtime_checkable
class ObjectStorage(Protocol):
    """Byte storage for images and evidence.

    In production this is S3 with SSE-KMS; in dev it is the local filesystem.
    Keys are tenant-prefixed by the caller, never by the adapter.
    """

    def put(
        self, key: str, data: bytes, content_type: str = "application/octet-stream"
    ) -> str:  # pragma: no cover
        """Store bytes and return the key."""
        ...

    def get(self, key: str) -> bytes:  # pragma: no cover
        """Fetch bytes, raising ``KeyError`` if absent."""
        ...

    def exists(self, key: str) -> bool:  # pragma: no cover
        """Whether the key is present."""
        ...

    def delete(self, key: str) -> None:  # pragma: no cover
        """Delete a key. Idempotent."""
        ...

    def list(self, prefix: str) -> list[str]:  # pragma: no cover
        """List keys under a prefix."""
        ...

    def presigned_url(self, key: str, expires_seconds: int = 300) -> str:  # pragma: no cover
        """Return a time-limited URL for direct browser access."""
        ...


# ---------------------------------------------------------------------------
# Time
# ---------------------------------------------------------------------------


@runtime_checkable
class Clock(Protocol):
    """Injected time source.

    Never call ``datetime.now()`` in domain code. Tests need to control time,
    and clock skew between edge and cloud silently corrupts lateness.
    """

    def now(self) -> object:  # pragma: no cover
        """Return a timezone-aware UTC datetime."""
        ...


# ---------------------------------------------------------------------------
# Hardware (edge side; implemented in Python 3.12 under ros_ws/)
# ---------------------------------------------------------------------------


@runtime_checkable
class Camera(Protocol):
    """A stills camera with controllable zoom, focus and exposure."""

    def capture_still(self, zoom: float, timeout_s: float) -> bytes:  # pragma: no cover
        """Return encoded JPEG bytes, or raise ``TimeoutError``."""
        ...

    def get_metadata(self) -> dict[str, float]:  # pragma: no cover
        """Return exposure, zoom, resolution as reported by the device."""
        ...

    def is_healthy(self) -> bool:  # pragma: no cover
        """Whether the device is currently reachable."""
        ...


@runtime_checkable
class Servo(Protocol):
    """A pan (and optionally tilt) actuator with hard limits."""

    def goto(self, angle_deg: float, speed: float, timeout_s: float) -> float:  # pragma: no cover
        """Move to an angle, returning the achieved angle."""
        ...

    def position(self) -> float:  # pragma: no cover
        """Current angle in degrees."""
        ...

    def home(self) -> float:  # pragma: no cover
        """Run the homing routine; returns the homed reference angle."""
        ...

    def stop(self) -> None:  # pragma: no cover
        """Emergency stop."""
        ...


# ---------------------------------------------------------------------------
# Messaging
# ---------------------------------------------------------------------------


@runtime_checkable
class JobQueue(Protocol):
    """Durable work queue.

    ``memory`` in dev/CI, ``sqs`` in production. The contract that matters is
    at-least-once delivery plus idempotent handling, because SQS cannot promise
    exactly-once.
    """

    def enqueue(self, payload: dict[str, object], dedup_key: str | None = None) -> str:  # pragma: no cover
        """Publish a job; returns a job id."""
        ...

    def consume(
        self, max_messages: int = 1, wait_s: int = 0
    ) -> list[tuple[str, dict[str, object]]]:  # pragma: no cover
        """Return ``(receipt, payload)`` pairs to process."""
        ...

    def acknowledge(self, receipt: str) -> None:  # pragma: no cover
        """Mark a job done."""
        ...

    def release(self, receipt: str, delay_s: int = 0) -> None:  # pragma: no cover
        """Return a job to the queue for retry."""
        ...


__all__ = [
    "Camera",
    "Clock",
    "Detector",
    "Embedder",
    "JobQueue",
    "LivenessChecker",
    "ObjectStorage",
    "Servo",
    "VectorIndex",
]
