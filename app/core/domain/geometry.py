"""Geometry: alignment, tiling, IoU, and the detect-then-embed convenience path.

Two things live here that are easy to get wrong and expensive to get wrong:

**Alignment.** The crop shown to an operator as evidence must be the *same*
pixels the embedder consumed. The legacy code saved a raw ``image.crop(bbox)``
while the embedding came from InsightFace's aligned 112x112 warp, so the
"evidence" was not what produced the decision (docs/00_audit.md 4.10). Here
:func:`aligned_crop` is the single function that produces the crop, and it is
the crop that gets stored.

**Tiling.** A 300-student classroom is photographed from the front, so back-row
faces are tiny. Running a detector on a downscaled full frame loses them. This
module tiles the frame into overlapping windows at a target resolution, runs
detection on each, maps boxes back to full-frame coordinates, and merges with
IoU-based NMS. The grid respects the frame's aspect ratio and is bounded so a
malformed upload cannot create unbounded inference calls.
"""

from __future__ import annotations

import logging
import math
from collections.abc import Iterator
from dataclasses import dataclass

import cv2
import numpy as np

from app.core.domain.types import BBox, FaceObservation, FloatArray, Keypoint

log = logging.getLogger(__name__)

#: Aligned crop size. Fixed by every recogniser in this project.
ALIGN_SIZE = 112

#: The five-landmark ArcFace template (left eye, right eye, nose, mouth-L,
#: mouth-R) mapped to a 112x112 crop. Used for the similarity transform.
_ARCFACE_TEMPLATE = np.array(
    [
        [38.2946, 51.6963],
        [73.5318, 51.5014],
        [56.0252, 71.7366],
        [41.5493, 92.3655],
        [70.7299, 92.2041],
    ],
    dtype=np.float32,
)

#: Minimum IoU for two detections to be considered the same face during merge.
DEFAULT_NMS_IOU = 0.4

#: A face below this fraction of the frame's short side is a probable duplicate
#: produced by a tile boundary rather than a real extra face.
_TINY_FACE_AREA_RATIO = 0.0004


@dataclass(frozen=True, slots=True)
class TileSpec:
    """One detection window, in full-frame coordinates."""

    index: int
    x0: int
    y0: int
    x1: int
    y1: int
    is_full_frame: bool = False

    @property
    def width(self) -> int:
        """Tile width in pixels."""
        return self.x1 - self.x0

    @property
    def height(self) -> int:
        """Tile height in pixels."""
        return self.y1 - self.y0


def iou(first: BBox, second: BBox) -> float:
    """Intersection over union of two boxes."""
    left, top = max(first[0], second[0]), max(first[1], second[1])
    right, bottom = min(first[2], second[2]), min(first[3], second[3])
    intersection = max(0, right - left) * max(0, bottom - top)
    if intersection == 0:
        return 0.0
    area_a = (first[2] - first[0]) * (first[3] - first[1])
    area_b = (second[2] - second[0]) * (second[3] - second[1])
    union = area_a + area_b - intersection
    return intersection / union if union else 0.0


def box_area(box: BBox) -> int:
    """Area of a box, clamped at zero."""
    return max(0, box[2] - box[0]) * max(0, box[3] - box[1])


def contains(outer: BBox, inner: BBox) -> bool:
    """Whether ``inner`` lies entirely within ``outer``."""
    return inner[0] >= outer[0] and inner[1] >= outer[1] and inner[2] <= outer[2] and inner[3] <= outer[3]


def choose_tile_grid(
    width: int,
    height: int,
    target_side: int,
    max_tiles: int,
    reserve: int = 1,
) -> tuple[int, int]:
    """Pick a ``(columns, rows)`` grid that is dense but aspect-faithful.

    The densest grid is preferred, because tile count drives small-face recall.
    Aspect fidelity is paid for out of density: a 4:3 frame tiled 5x1 would be
    five very wide, thin strips, and the faces inside them would be squashed.

    Two bounds, both deliberate:

    * The search never goes beyond ``ceil(side / target_side)``, so a tile is
      never **smaller** than ``target_side``. Finer tiles would find smaller
      faces, but only by spending inference calls the budget does not have, and
      the scan planner's zoom pass is the correct tool for that job.
    * ``reserve`` holds back windows before the grid is chosen, so the
      full-frame pass is counted against ``max_tiles``.

    Args:
        width: Frame width in pixels.
        height: Frame height in pixels.
        target_side: Desired tile side in pixels; also the minimum.
        max_tiles: Hard cap on the TOTAL number of detection windows.
        reserve: Windows consumed by something other than the grid.

    Returns:
        ``(columns, rows)`` such that ``columns * rows + reserve <= max_tiles``.
    """
    budget = max(1, max_tiles - max(0, reserve))
    max_columns = max(1, math.ceil(width / target_side))
    max_rows = max(1, math.ceil(height / target_side))
    if max_columns * max_rows <= budget:
        return max_columns, max_rows

    target_ratio = width / height if height else 1.0
    candidates = [
        (columns, rows)
        for columns in range(1, max_columns + 1)
        for rows in range(1, max_rows + 1)
        if columns * rows <= budget
    ]
    if not candidates:  # pragma: no cover - max_tiles >= 1 is validated in config
        return 1, 1

    def score(grid: tuple[int, int]) -> float:
        """Denser is better, but aspect fidelity is paid for out of density.

        Ranking purely by tile count picked 3x1 grids for 16:9 frames -- three
        very tall, thin tiles that waste most of the frame. Subtracting the
        log-aspect mismatch (weight 1.0) makes a slightly sparser but
        aspect-faithful grid win, which is what "faithful" was always meant to
        mean in the first draft of this function.
        """
        columns, rows = grid
        mismatch = abs(math.log((columns / rows) / target_ratio))
        return columns * rows - mismatch

    return max(candidates, key=score)


def plan_tiles(
    width: int,
    height: int,
    target_side: int,
    overlap_ratio: float,
    max_tiles: int,
    include_full_frame: bool = True,
) -> list[TileSpec]:
    """Build the detection plan for one frame.

    The full-frame pass is always included when tiling is active. It catches
    large faces that straddle a tile boundary and that aggressive downscaling in
    a tile would have handled anyway; the tiles then recover the small faces the
    full frame loses. NMS merges the two result sets.

    Args:
        include_full_frame: Disable for a zoom pass, where the full frame is
            already covered by a coarser pass.

    Returns:
        Ordered tiles, full frame first.
    """
    if not 0 <= overlap_ratio < 1:
        raise ValueError(f"overlap_ratio must be in [0, 1), got {overlap_ratio}")

    columns, rows = choose_tile_grid(
        width, height, target_side, max_tiles, reserve=1 if include_full_frame else 0
    )
    tile_h = math.ceil(height / rows)
    tile_w = math.ceil(width / columns)
    overlap_h = int(tile_h * overlap_ratio)
    overlap_w = int(tile_w * overlap_ratio)

    tiles: list[TileSpec] = []
    if include_full_frame:
        tiles.append(TileSpec(index=0, x0=0, y0=0, x1=width, y1=height, is_full_frame=True))
    index = 1
    for row in range(rows):
        for column in range(columns):
            x0, y0 = column * tile_w, row * tile_h
            # The final tile is extended rather than shrunk, so the far edge of
            # the frame is always covered and no strip is left undetected.
            x1 = min(width, x0 + tile_w + overlap_w)
            y1 = min(height, y0 + tile_h + overlap_h)
            if x1 <= x0 or y1 <= y0:
                continue
            tiles.append(TileSpec(index=index, x0=x0, y0=y0, x1=x1, y1=y1))
            index += 1
    return tiles


def iter_tile_images(image: np.ndarray, tiles: list[TileSpec]) -> Iterator[tuple[TileSpec, np.ndarray]]:
    """Yield ``(tile, image_slice)`` for each tile."""
    for tile in tiles:
        yield tile, image[tile.y0 : tile.y1, tile.x0 : tile.x1]


def offset_box(box: BBox, dx: int, dy: int) -> BBox:
    """Translate a box by a pixel offset."""
    return (box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy)


def offset_keypoints(points: np.ndarray, dx: int, dy: int) -> np.ndarray:
    """Translate a landmark array by a pixel offset."""
    if points.size == 0:
        return points
    return np.asarray(points + np.array([dx, dy], dtype=points.dtype))


def merge_detections(
    observations: list[FaceObservation],
    iou_threshold: float = DEFAULT_NMS_IOU,
    frame_area: int | None = None,
) -> list[FaceObservation]:
    """Greedy non-maximum suppression across overlapping tiles.

    Sorted by detector score, keeping the strongest box of each cluster. This
    is what stops one face seen in three overlapping tiles becoming three
    attendance events.

    Args:
        frame_area: Frame area in pixels. When given, detections below
            ``_TINY_FACE_AREA_RATIO`` of it are dropped as tile-boundary
            artefacts, provided a larger detection overlaps them.
    """
    if not observations:
        return []

    ordered = sorted(observations, key=lambda o: o.detector_score, reverse=True)
    kept: list[FaceObservation] = []
    for candidate in ordered:
        overlapping = [k for k in kept if iou(candidate.bbox, k.bbox) > iou_threshold]
        if overlapping:
            # A tiny box inside a much larger kept box is a boundary artefact
            # from a tile edge, not a second person.
            if frame_area and candidate_is_tiny_artefact(candidate, overlapping, frame_area):
                log.debug(
                    "dropped tile-boundary artefact",
                    extra={"bbox": candidate.bbox, "score": candidate.detector_score},
                )
            continue

        # No IoU overlap. A containment test is still needed: a 4px box inside a
        # 100px box has IoU 0.0016, far below any NMS threshold, so an
        # overlap-only test let tile-boundary artefacts through as extra people.
        containers = [k for k in kept if contains(k.bbox, candidate.bbox)]
        if frame_area and containers and candidate_is_tiny_artefact(candidate, containers, frame_area):
            log.debug(
                "dropped contained tile-boundary artefact",
                extra={"bbox": candidate.bbox, "score": candidate.detector_score},
            )
            continue

        kept.append(candidate)
    return kept


def candidate_is_tiny_artefact(
    candidate: FaceObservation,
    overlapping: list[FaceObservation],
    frame_area: int,
) -> bool:
    """Whether a small overlapping box is a duplicate rather than a real face."""
    if box_area(candidate.bbox) > frame_area * _TINY_FACE_AREA_RATIO:
        return False
    return any(contains(k.bbox, candidate.bbox) for k in overlapping)


def landmarks_to_keypoints(points: np.ndarray) -> tuple[Keypoint, ...]:
    """Convert an ``(N, 2)`` array to Keypoint tuples."""
    return tuple(Keypoint(x=float(p[0]), y=float(p[1])) for p in np.asarray(points).reshape(-1, 2))


def estimate_pose(
    landmarks: np.ndarray,
    bbox: BBox | None = None,  # noqa: ARG001 - call-site symmetry; unused
    reference: np.ndarray | None = None,
) -> tuple[float, float, float]:
    """Estimate ``(yaw, pitch, roll)`` in degrees from 2-D landmarks.

    A full solve needs 3-D landmarks or a PnP pass. This is a cheap geometric
    approximation good enough for a *quality gate* (reject wildly turned heads),
    which is all it is used for. It is explicitly not a gaze or a precise pose
    estimate, and is labelled as an approximation wherever it is reported.

    Args:
        bbox: Accepted for call-site symmetry with other geometry helpers;
            not needed, since the five landmarks carry all the information.

    Returns:
        ``(yaw, pitch, roll)`` in degrees, all near 0 for a frontal face.
    """
    pts = np.asarray(landmarks, dtype=np.float32).reshape(-1, 2)
    if pts.shape[0] < 5:
        return 0.0, 0.0, 0.0

    left_eye, right_eye, nose = pts[0], pts[1], pts[2]
    mouth_l, mouth_r = pts[3], pts[4]

    # Roll: angle of the eye line away from horizontal.
    roll = math.degrees(math.atan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0]))

    eye_mid = (left_eye + right_eye) / 2.0
    mouth_mid = (mouth_l + mouth_r) / 2.0

    # Interocular distance is the scale reference; the face is roughly 2 eyes
    # wide and ~2.4 eyes from eyes to mouth when frontal.
    iod = float(np.linalg.norm(right_eye - left_eye))
    if iod < 1e-3:
        return 0.0, 0.0, roll

    eye_to_nose = float(np.linalg.norm(nose - eye_mid))
    eye_to_mouth = float(np.linalg.norm(mouth_mid - eye_mid))

    # As the head turns, the nose shifts laterally relative to the eye midpoint.
    yaw = math.degrees(math.atan2(nose[0] - eye_mid[0], max(1e-3, abs(nose[1] - eye_mid[1]))))
    # As the head pitches, the eyes-to-mouth distance shortens.
    pitch_ratio = eye_to_mouth / max(1e-3, 2.4 * iod)
    pitch = math.degrees((pitch_ratio - 1.0) * 45.0)

    if reference is not None:
        ref = np.asarray(reference, dtype=np.float32).reshape(-1, 2)
        yaw -= 0.0  # no reference template shipped; kept for future use
        del ref

    del eye_to_nose
    return (yaw, pitch, roll)


def aligned_crop(
    image_bgr: np.ndarray,
    landmarks: np.ndarray,
    size: int = ALIGN_SIZE,
) -> np.ndarray:
    """Warp landmarks to the canonical ``size x size`` template.

    This is the crop the embedder consumes **and** the crop stored as
    evidence, so an operator reviewing a decision is looking at exactly the
    pixels that produced it.

    Args:
        image_bgr: Source image in BGR.
        landmarks: ``(5, 2)`` array in source-image coordinates.
        size: Output side. 112 for every current recogniser.

    Returns:
        A ``size x size`` uint8 BGR crop.
    """
    pts = np.asarray(landmarks, dtype=np.float32).reshape(-1, 2)
    if pts.shape[0] != 5:
        raise ValueError(f"expected 5 landmarks, got {pts.shape[0]}")

    template = _ARCFACE_TEMPLATE * (size / ALIGN_SIZE)
    matrix = cv2.estimateAffinePartial2D(pts, template, method=cv2.LMEDS)[0]
    if matrix is None:
        # A degenerate landmark set (collinear points) breaks the solve. Fall
        # back to a plain resize of the bounding box rather than failing the
        # whole frame for one bad detection.
        log.warning("landmark alignment failed; falling back to a box resize")
        x1, y1, x2, y2 = (
            int(pts[:, 0].min()),
            int(pts[:, 1].min()),
            int(pts[:, 0].max()),
            int(pts[:, 1].max()),
        )
        x2, y2 = max(x2, x1 + 1), max(y2, y1 + 1)
        return cv2.resize(image_bgr[y1:y2, x1:x2], (size, size), interpolation=cv2.INTER_AREA)

    return cv2.warpAffine(
        image_bgr,
        matrix,
        (size, size),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=0,
    )


def detect_and_embed(image_bgr: np.ndarray) -> FloatArray | None:
    """Detect the largest face in a BGR image and return its embedding.

    A convenience path for enrollment and benchmarking, where exactly one
    dominant face is expected. Returns ``None`` when no face clears the
    configured thresholds. Never guesses: a classroom frame with many equally
    large faces returns ``None`` rather than an arbitrary one.
    """
    from app.core.config import settings
    from app.registry.loader import load_registry

    registry = load_registry()
    detections = registry.detector.detect(image_bgr)
    usable = [
        d
        for d in detections
        if d[2] >= settings.min_detection_score
        and (d[0][2] - d[0][0]) >= settings.min_face_size_px
        and (d[0][3] - d[0][1]) >= settings.min_face_size_px
    ]
    if not usable:
        return None
    usable.sort(key=lambda d: box_area(d[0]), reverse=True)
    _bbox, landmarks, _score = usable[0]
    if len(usable) > 1:
        largest = box_area(usable[0][0])
        second = box_area(usable[1][0])
        if largest < 2.5 * second:
            log.debug("refusing to pick a dominant face: top two are comparable")
            return None
    crop = aligned_crop(image_bgr, landmarks)
    return np.asarray(registry.embedder.embed(crop), dtype=np.float32)


__all__ = [
    "ALIGN_SIZE",
    "DEFAULT_NMS_IOU",
    "TileSpec",
    "aligned_crop",
    "box_area",
    "choose_tile_grid",
    "contains",
    "detect_and_embed",
    "estimate_pose",
    "iou",
    "iter_tile_images",
    "landmarks_to_keypoints",
    "merge_detections",
    "offset_box",
    "offset_keypoints",
    "plan_tiles",
]
