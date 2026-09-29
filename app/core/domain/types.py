"""Core value types shared across the framework-free domain layer.

Nothing in :mod:`app.core` may import FastAPI, SQLAlchemy, ROS or a concrete
model runtime. These are the only shapes the domain logic needs to speak.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

import numpy as np
from numpy.typing import NDArray

FloatArray = NDArray[np.float32]
BBox = tuple[int, int, int, int]  # x1, y1, x2, y2 in source-image pixels


class Decision(StrEnum):
    """What the identity engine concluded about one detected face.

    The three values are exhaustive and mutually exclusive by construction, so
    a face can never be simultaneously "confirmed" and "queued for review".
    """

    #: Matched the gallery above the high threshold AND the margin rule.
    CONFIRMED = "confirmed"
    #: A plausible candidate, but not enough to act on unattended. A human
    #: is asked to confirm or correct it.
    UNCERTAIN = "uncertain"
    #: No usable candidate. Must be queued for a human. Never guessed.
    UNKNOWN = "unknown"


class Route(StrEnum):
    """How a face was persisted, which is not the same as :class:`Decision`."""

    AUTO = "auto"  # confirmed unattended
    CONFIRM = "low_conf_confirm"  # uncertain, best guess shown to operator
    REVIEW = "review"  # unknown, operator must identify
    MANUAL_LABEL = "manual_label"  # a human named this face
    DISMISSED = "dismissed"  # a human rejected this face (visitor, artefact)


#: Match types that constitute a *confirmed* attendance decision.
#: Nothing else may ever be reported as present.
CONFIRMED_MATCH_TYPES: frozenset[str] = frozenset({Route.AUTO.value, Route.MANUAL_LABEL.value})


class Quality(StrEnum):
    """Coarse quality verdict driving re-capture versus recognition."""

    GOOD = "good"
    POOR = "poor"
    REJECT = "reject"


@dataclass(frozen=True, slots=True)
class Keypoint:
    """A 2-D landmark in source-image pixel coordinates."""

    x: float
    y: float


@dataclass(frozen=True, slots=True)
class FaceObservation:
    """A single face seen in a single frame, before any identity decision.

    Coordinates are always in source-image pixels. ``aligned_crop`` is the
    112x112 warp the embedder actually consumed, kept so the evidence shown to
    an operator is byte-identical to the pixels that produced the embedding.
    """

    bbox: BBox
    landmarks: tuple[Keypoint, ...]
    detector_score: float
    aligned_crop: bytes | None = None
    pose: tuple[float, float, float] = (0.0, 0.0, 0.0)  # (yaw, pitch, roll) degrees
    sharpness: float = 0.0
    mean_luma: float = 0.0
    luma_stddev: float = 0.0

    @property
    def width(self) -> int:
        """Bounding-box width in pixels."""
        return self.bbox[2] - self.bbox[0]

    @property
    def height(self) -> int:
        """Bounding-box height in pixels."""
        return self.bbox[3] - self.bbox[1]


@dataclass(frozen=True, slots=True)
class MatchCandidate:
    """One gallery entry that matched a query embedding."""

    roll_no: str
    score: float
    gallery_id: int


@dataclass(frozen=True, slots=True)
class IdentityDecision:
    """The identity engine's verdict on one face."""

    decision: Decision
    #: Best candidate, or ``None`` when nothing cleared ``low``.
    best: MatchCandidate | None
    #: Runner-up. Present whenever the gallery had at least two candidates,
    #: and required for the margin rule.
    runner_up: MatchCandidate | None
    #: Why this decision was reached. Persisted for threshold calibration.
    reason: str
    #: Set when the face is queued for a human.
    queue_for_review: bool = False

    @property
    def roll_no(self) -> str | None:
        """Best-guess roll number, or ``None`` when there is no usable guess.

        Even for ``UNCERTAIN`` this is populated so the operator can be asked
        "is this Priya?". It is never treated as attendance on its own.
        """
        return self.best.roll_no if self.best else None

    @property
    def score(self) -> float:
        """Cosine similarity of the best candidate, or 0.0."""
        return self.best.score if self.best else 0.0

    @property
    def margin(self) -> float:
        """Gap between the best and the runner-up.

        A small margin means the identity decision was a coin flip regardless
        of how high the top score is. See docs/00_audit.md §4.3.
        """
        if self.best is None:
            return 0.0
        if self.runner_up is None:
            return self.best.score
        return self.best.score - self.runner_up.score


@dataclass(frozen=True, slots=True)
class GalleryEntry:
    """A stored embedding plus its provenance."""

    gallery_id: int
    roll_no: str
    embedding: FloatArray
    source_image_path: str
    added_via: str
    added_at: Any


@dataclass(frozen=True, slots=True)
class FrameContext:
    """Metadata about one ingested frame, propagated end to end for tracing."""

    frame_id: str
    session_id: int
    tenant_id: str
    captured_at: Any
    camera_angle_deg: float | None = None
    zoom: float | None = None
    width: int = 0
    height: int = 0
    #: Correlates this frame across edge, queue, worker and decision.
    correlation_id: str = ""
    extra: dict[str, Any] = field(default_factory=dict)


__all__ = [
    "CONFIRMED_MATCH_TYPES",
    "BBox",
    "Decision",
    "FaceObservation",
    "FloatArray",
    "FrameContext",
    "GalleryEntry",
    "IdentityDecision",
    "Keypoint",
    "MatchCandidate",
    "Quality",
    "Route",
]
