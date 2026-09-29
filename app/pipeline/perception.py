"""Perception pipeline: tiles -> detect -> quality -> align -> embed.

This is the W2 wiring layer. It replaces the legacy
``app/services/attendance.py`` detection path with one that:

* decodes through the audited boundary (:mod:`app.core.domain.imageops`), so
  channel order and EXIF orientation are handled once, in one place;
* applies the detector's working-size downscale, and maps boxes back;
* runs a face-quality gate before embedding, so a blurry 30 px face is not
  turned into a confident-looking embedding (docs/00_audit.md 4.8);
* stores the **aligned** crop as evidence, so what an operator reviews is what
  the model consumed (4.10);
* embeds in one batch per frame, which is the only way ArcFace-style models
  amortise their cost;
* is bounded by ``max_tiles`` and by the quality gate, so a hostile upload
  cannot create unbounded inference work.

Pure with respect to ROS and HTTP: it takes bytes and returns a result object.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

import numpy as np

from app.core.domain import imageops
from app.core.domain.geometry import (
    aligned_crop,
    box_area,
    iter_tile_images,
    landmarks_to_keypoints,
    merge_detections,
    offset_box,
    offset_keypoints,
    plan_tiles,
)
from app.core.domain.quality import Quality, QualityThresholds, assess
from app.core.domain.types import FaceObservation, FloatArray, FrameContext

log = logging.getLogger(__name__)


@dataclass(slots=True)
class DetectedFaceResult:
    """One face that survived detection and the quality gate.

    Attributes:
        observation: Geometry, landmarks and measured quality metrics.
        embedding: L2-normalised embedding, or ``None`` if the face was too
            poor to embed.
        aligned_crop: The exact bytes the embedder consumed, and what gets
            stored as evidence.
        quality: The quality verdict.
        tile_index: Which detection tile found it. Kept for diagnosis: a face
            only ever found by one tile at the frame edge may be a boundary
            artefact.
    """

    observation: FaceObservation
    embedding: FloatArray | None
    aligned_crop: bytes
    quality: Any
    tile_index: int = 0

    @property
    def can_auto_confirm(self) -> bool:
        """Whether this face may produce an unattended attendance decision."""
        return self.embedding is not None and bool(self.quality.can_auto_confirm)

    @property
    def needs_recapture(self) -> bool:
        """Whether the scan planner should come back at higher zoom."""
        return bool(self.quality.needs_recapture)


@dataclass(slots=True)
class FrameResult:
    """Everything one frame produced.

    Attributes:
        faces: Faces that passed the quality gate.
        rejected: Faces discarded, with the reason, so coverage is diagnosable
            rather than mysterious.
        recapture_regions: Boxes worth re-shooting at higher zoom.
        metadata: Decode provenance (EXIF, dimensions).
        timings_ms: Per-stage timings, for the benchmark and for tracing.
    """

    context: FrameContext
    image: np.ndarray
    faces: list[DetectedFaceResult] = field(default_factory=list)
    rejected: list[tuple[FaceObservation, str]] = field(default_factory=list)
    recapture_regions: list[tuple[int, int, int, int]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    timings_ms: dict[str, float] = field(default_factory=dict)


def _measure(observation: FaceObservation, crop_bgr: np.ndarray) -> FaceObservation:
    """Fill in the measured quality metrics of an observation.

    Uses ``dataclasses.replace`` on the frozen type so the geometry is
    unchanged and only the measurements are added.
    """
    from dataclasses import replace

    mean_luma, luma_stddev = imageops.illumination_stats(crop_bgr)
    return replace(
        observation,
        sharpness=imageops.sharpness_score(crop_bgr),
        mean_luma=mean_luma,
        luma_stddev=luma_stddev,
    )


def process_frame_bytes(
    data: bytes,
    context: FrameContext,
    *,
    thresholds: QualityThresholds | None = None,
    max_tiles: int | None = None,
    tile_target_side: int | None = None,
    overlap_ratio: float | None = None,
    store_evidence_crops: bool = True,
) -> FrameResult:
    """Run the full per-frame pipeline on encoded image bytes.

    Args:
        data: Encoded image bytes.
        context: Frame provenance, for tracing and persistence.
        thresholds: Quality gates; defaults to application settings.
        max_tiles, tile_target_side, overlap_ratio: Tiling overrides.
        store_evidence_crops: When False, aligned crops are not JPEG-encoded.
            Detection-only passes (e.g. a cheap wide pass) use this to skip
            the encode cost.

    Returns:
        A :class:`FrameResult`.

    Raises:
        ImageDecodeError: the bytes are not a decodable, safe image.
    """
    from app.core.config import settings

    thresholds = thresholds or QualityThresholds.from_settings()
    cap = max_tiles if max_tiles is not None else settings.max_detection_tiles
    target = tile_target_side if tile_target_side is not None else settings.tile_target_side_px
    overlap = overlap_ratio if overlap_ratio is not None else settings.tiling_overlap_ratio

    timings: dict[str, float] = {}

    start = time.perf_counter()
    image, metadata = imageops.decode(data, max_pixels=settings.max_image_pixels)
    timings["decode_ms"] = (time.perf_counter() - start) * 1000.0

    from app.registry.loader import load_registry

    registry = load_registry()
    height, width = image.shape[:2]

    # --- Detect ---------------------------------------------------------
    start = time.perf_counter()
    # A frame below the tiling threshold is small enough that downscaling for
    # the detector loses nothing, so it gets a single pass. Tiling it anyway
    # doubled the detector work on every 640x480 frame, which is a real
    # regression the legacy code did not have.
    if max(height, width) <= settings.tiling_threshold_px:
        tiles = plan_tiles(width, height, target, overlap, cap, include_full_frame=False)
    else:
        tiles = plan_tiles(width, height, target, overlap, cap)
    observations: list[FaceObservation] = []
    tile_of: dict[int, int] = {}
    raw: list[FaceObservation] = []
    for tile, tile_image in iter_tile_images(image, tiles):
        for bbox, landmarks, score in registry.detector.detect(tile_image):
            full_box = offset_box(bbox, tile.x0, tile.y0)
            full_landmarks = offset_keypoints(landmarks, tile.x0, tile.y0)
            observation = FaceObservation(
                bbox=full_box,
                landmarks=landmarks_to_keypoints(full_landmarks),
                detector_score=score,
            )
            raw.append(observation)
            if len(raw) == len(observations) + 1:
                tile_of[id(observation)] = tile.index
            observations.append(observation)

    merged = merge_detections(raw, frame_area=width * height)
    timings["detect_ms"] = (time.perf_counter() - start) * 1000.0

    # --- Quality gate, align, measure -----------------------------------
    start = time.perf_counter()
    survivors: list[DetectedFaceResult] = []
    rejected: list[tuple[FaceObservation, str]] = []
    recapture: list[tuple[int, int, int, int]] = []

    for observation in merged:
        landmarks = np.array([[p.x, p.y] for p in observation.landmarks], dtype=np.float32)
        if landmarks.shape[0] != 5:
            rejected.append((observation, "landmarks_unavailable"))
            continue

        try:
            crop = aligned_crop(image, landmarks)
        except imageops.ImageDecodeError as exc:
            rejected.append((observation, f"align_failed:{exc}"))
            continue

        measured = _measure(observation, crop)
        report = assess(measured, thresholds)

        if report.quality is Quality.REJECT:
            rejected.append((measured, ",".join(report.reasons)))
            continue

        if report.needs_recapture:
            recapture.append(measured.bbox)

        embedding: FloatArray | None = None
        try:
            embedding = registry.embedder.embed(crop)
        except Exception as exc:  # noqa: BLE001 - one bad face must not fail the frame
            log.warning(
                "embedding failed for one face",
                extra={"bbox": measured.bbox, "error": f"{type(exc).__name__}"},
            )
            rejected.append((measured, f"embed_failed:{type(exc).__name__}"))
            continue

        evidence = imageops.encode_jpeg(crop) if store_evidence_crops else b""
        survivors.append(
            DetectedFaceResult(
                observation=measured,
                embedding=embedding,
                aligned_crop=evidence,
                quality=report,
                tile_index=tile_of.get(id(observation), 0),
            )
        )
    timings["quality_align_embed_ms"] = (time.perf_counter() - start) * 1000.0

    del tile_of, observations
    return FrameResult(
        context=context,
        image=image,
        faces=survivors,
        rejected=rejected,
        recapture_regions=recapture,
        metadata=metadata,
        timings_ms=timings,
    )


def coverage_stats(result: FrameResult, expected_students: int | None = None) -> dict[str, float]:
    """Summarise what a frame achieved, for the coverage acceptance metric.

    ``coverage`` is the fraction of expected students who produced at least one
    usable face. It is the single most important number in the whole system and
    it is only meaningful when ``expected_students`` is supplied from the
    roster, which is why it is optional.
    """
    usable = [f for f in result.faces if f.embedding is not None]
    auto_ok = [f for f in usable if f.can_auto_confirm]
    stats = {
        "faces_detected": float(len(usable) + len(result.rejected)),
        "faces_usable": float(len(usable)),
        "faces_rejected": float(len(result.rejected)),
        "faces_auto_confirmable": float(len(auto_ok)),
        "recapture_regions": float(len(result.recapture_regions)),
    }
    if expected_students:
        stats["coverage"] = min(1.0, len(usable) / float(expected_students))
    largest = max((box_area(f.observation.bbox) ** 0.5 for f in usable), default=0.0)
    stats["median_face_px"] = largest
    return stats


__all__ = [
    "DetectedFaceResult",
    "FrameResult",
    "coverage_stats",
    "process_frame_bytes",
]
