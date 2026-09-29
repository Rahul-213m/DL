"""Face quality assessment.

A blurred, tiny or badly lit face produces a confident-looking embedding that
means nothing. The legacy pipeline had no quality gate at all: any detection
above 40 px was embedded and matched, and ``det_score`` was captured but never
used as a filter (docs/00_audit.md 4.8).

The distinction that matters:

* **REJECT** - the face cannot yield a usable embedding. Do not match it; ask
  for a better capture.
* **POOR** - an embedding may be computed, but the result should not be allowed
  to *auto-confirm* attendance. It can still be shown to a human as a guess.
* **GOOD** - normal path.

That middle tier is the important one. Throwing away every imperfect face would
gut coverage in a real classroom; matching them confidently would produce false
attendance. Neither is acceptable, so poor faces are demoted rather than
discarded.

Thresholds are **not calibrated defaults**. They are starting points to be
replaced by ``scripts/calibrate_quality.py`` on real classroom data, and every
place they are used says so.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.domain.types import FaceObservation, Quality

#: A face narrower than this is rejected outright: below it, the landmark
#: solver has too few pixels to place eyes and nose reliably.
REJECT_FACE_WIDTH_PX = 24

#: Below this, ask the scan planner to zoom in rather than give up.
POOR_FACE_WIDTH_PX = 64

#: The stated recognition target. Above this, quality is rarely the limiter.
GOOD_FACE_WIDTH_PX = 80


@dataclass(frozen=True, slots=True)
class QualityThresholds:
    """Configurable quality gates.

    Attributes:
        min_width_px: Below this the face is REJECTed.
        poor_width_px: Below this the face is POOR and cannot auto-confirm.
        min_sharpness: Variance-of-Laplacian floor. NOT calibrated.
        max_yaw_deg, max_pitch_deg, max_roll_deg: Pose limits.
        min_mean_luma, min_luma_stddev: Illumination floors.
        min_detector_score: Confidence floor for accepting a detection at all.
    """

    min_width_px: int = REJECT_FACE_WIDTH_PX
    poor_width_px: int = POOR_FACE_WIDTH_PX
    min_sharpness: float = 40.0
    max_yaw_deg: float = 35.0
    max_pitch_deg: float = 25.0
    max_roll_deg: float = 20.0
    min_mean_luma: float = 40.0
    min_luma_stddev: float = 15.0
    min_detector_score: float = 0.70

    @classmethod
    def from_settings(cls) -> QualityThresholds:
        """Build thresholds from application settings."""
        from app.core.config import settings

        return cls(
            min_width_px=REJECT_FACE_WIDTH_PX,
            poor_width_px=settings.rescan_face_width_px,
            min_sharpness=settings.min_sharpness_score,
            max_yaw_deg=settings.max_pose_yaw_deg,
            max_pitch_deg=settings.max_pose_pitch_deg,
            max_roll_deg=settings.max_pose_roll_deg,
            min_mean_luma=settings.min_mean_luma,
            min_luma_stddev=settings.min_luma_stddev,
            min_detector_score=settings.min_detection_score,
        )


@dataclass(frozen=True, slots=True)
class QualityReport:
    """Per-face quality verdict with the reasons that produced it.

    Reasons are accumulated rather than short-circuited, so an operator can see
    *everything* wrong with a capture, not just the first thing checked.
    """

    quality: Quality
    reasons: tuple[str, ...] = ()
    #: True when the face is too small or too poor to trust, so the scan
    #: planner should capture the region again at higher zoom.
    needs_recapture: bool = False
    metrics: dict[str, float] = field(default_factory=dict)

    @property
    def is_usable(self) -> bool:
        """Whether an embedding may be computed at all."""
        return self.quality is not Quality.REJECT

    @property
    def can_auto_confirm(self) -> bool:
        """Whether this face is good enough to mark attendance unattended.

        POOR faces may still be *matched*, but their match may only ever
        produce an UNCERTAIN decision that goes to a human.
        """
        return self.quality is Quality.GOOD


def assess(face: FaceObservation, thresholds: QualityThresholds | None = None) -> QualityReport:
    """Assess one face observation.

    Args:
        face: The observation, already carrying sharpness and luma measured by
            the caller (measuring here would require the pixels, which this
            framework-free module does not hold).
        thresholds: Gate values; defaults to application settings.

    Returns:
        A report whose ``quality`` drives the decision, and whose
        ``needs_recapture`` drives the scan planner.
    """
    t = thresholds or QualityThresholds.from_settings()
    reasons: list[str] = []
    metrics: dict[str, float] = {
        "width_px": float(face.width),
        "detector_score": face.detector_score,
        "sharpness": face.sharpness,
        "mean_luma": face.mean_luma,
        "luma_stddev": face.luma_stddev,
        "yaw_deg": face.pose[0],
        "pitch_deg": face.pose[1],
        "roll_deg": face.pose[2],
    }

    # --- Size ------------------------------------------------------------
    if face.width < t.min_width_px:
        reasons.append(f"face_too_small:{face.width}px<{t.min_width_px}px")
        return QualityReport(Quality.REJECT, tuple(reasons), True, metrics)

    # --- Detector confidence --------------------------------------------
    if face.detector_score < t.min_detector_score:
        reasons.append(f"low_detector_score:{face.detector_score:.2f}<{t.min_detector_score:.2f}")
        return QualityReport(Quality.REJECT, tuple(reasons), False, metrics)

    needs_recapture = False

    if face.width < t.poor_width_px:
        reasons.append(f"small_face:{face.width}px<{t.poor_width_px}px")
        needs_recapture = True

    # --- Blur ------------------------------------------------------------
    if face.sharpness < t.min_sharpness:
        reasons.append(f"blurry:{face.sharpness:.1f}<{t.min_sharpness:.1f}")
        needs_recapture = True

    # --- Pose ------------------------------------------------------------
    yaw, pitch, roll = face.pose
    if abs(yaw) > t.max_yaw_deg:
        reasons.append(f"yaw:{yaw:.0f}deg>{t.max_yaw_deg:.0f}deg")
    if abs(pitch) > t.max_pitch_deg:
        reasons.append(f"pitch:{pitch:.0f}deg>{t.max_pitch_deg:.0f}deg")
    if abs(roll) > t.max_roll_deg:
        reasons.append(f"roll:{roll:.0f}deg>{t.max_roll_deg:.0f}deg")

    # --- Illumination ----------------------------------------------------
    if face.mean_luma < t.min_mean_luma:
        reasons.append(f"underlit:mean_luma={face.mean_luma:.0f}<{t.min_mean_luma:.0f}")
        needs_recapture = True
    if face.luma_stddev < t.min_luma_stddev:
        reasons.append(f"flat_lighting:stddev={face.luma_stddev:.0f}<{t.min_luma_stddev:.0f}")
        needs_recapture = True

    if not reasons:
        return QualityReport(Quality.GOOD, (), False, metrics)

    return QualityReport(Quality.POOR, tuple(reasons), needs_recapture, metrics)


def illumination_is_acceptable(mean_luma: float, stddev: float, t: QualityThresholds) -> bool:
    """Whether the whole FRAME is acceptably lit.

    Separate from per-face assessment: if the room is dark, every face will be
    poor and re-capturing individually will not help. The scan planner needs to
    know to wait for the lights instead.
    """
    return mean_luma >= t.min_mean_luma and stddev >= t.min_luma_stddev


def coverage_target_px() -> int:
    """The face width the system aims for, from configuration."""
    from app.core.config import settings

    return settings.rescan_face_width_px


__all__ = [
    "GOOD_FACE_WIDTH_PX",
    "POOR_FACE_WIDTH_PX",
    "REJECT_FACE_WIDTH_PX",
    "QualityReport",
    "QualityThresholds",
    "assess",
    "coverage_target_px",
    "illumination_is_acceptable",
]
