"""Score populations for threshold calibration, drawn from real evidence.

THE CIRCULARITY THIS AVOIDS
--------------------------
The obvious way to calibrate is to take every attendance event, call its
``roll_no`` ground truth, and measure. That is circular and it will flatter
the model, because the events in the table are exactly the ones the current
thresholds let through: the hard cases were either discarded or parked in the
review queue. Calibrating on that population re-measures the thresholds
instead of testing them.

So this module uses only **human-labelled** evidence as the query side:

* ``match_type == 'manual_label'`` -- a teacher or admin said who this was;
* any event whose ``cluster_id`` a resolved review item points at.

Those labels come from a person, not from the score being calibrated. An
auto-confirmed match is deliberately excluded, and the exclusion is logged, so
nobody mistakes a threshold report for an independent evaluation.

Negatives are then generated honestly: a labelled sighting compared against
**other** students' gallery vectors. With ``N`` students and ``G`` exemplars
each, one labelled sighting yields ``(N-1) * G`` impostor comparisons, which is
how a classroom-sized deployment reaches thousands of negatives from a handful
of labelled sessions.

Every figure this produces is a MEASUREMENT of the data available in this
database, and is only as good as that data. Nothing here extrapolates.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.domain.calibration import CalibrationReport, calibrate
from app.core.domain.types import FloatArray

log = logging.getLogger(__name__)

#: ``match_type`` values whose identity came from a person rather than a score.
HUMAN_LABELLED_MATCH_TYPES = ("manual_label", "cluster_label")


@dataclass(frozen=True, slots=True)
class ScorePopulations:
    """Positive and negative similarity scores, plus their provenance.

    Attributes:
        positives: Labelled sighting vs that student's own gallery.
        negatives: Labelled sighting vs other students' gallery.
        labelled_sightings: How many human-labelled sightings were used.
        gallery_students: How many distinct identities contributed negatives.
        excluded_auto: How many events were skipped for being auto-confirmed.
        excluded_no_label: How many skipped for having no identity at all.
        by_distance: Optional per-bucket positives, for the per-distance report.
    """

    positives: tuple[float, ...] = ()
    negatives: tuple[float, ...] = ()
    labelled_sightings: int = 0
    gallery_students: int = 0
    excluded_auto: int = 0
    excluded_no_label: int = 0
    by_distance: dict[str, tuple[float, ...]] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """JSON-serialisable provenance, for the report file."""
        return {
            "positives": len(self.positives),
            "negatives": len(self.negatives),
            "labelled_sightings": self.labelled_sightings,
            "gallery_students": self.gallery_students,
            "excluded_auto_confirmed": self.excluded_auto,
            "excluded_without_identity": self.excluded_no_label,
            "by_distance": {k: len(v) for k, v in self.by_distance.items()},
        }


def _unpack(blob: bytes) -> FloatArray:
    vector = np.frombuffer(blob, dtype=np.float32)
    norm = float(np.linalg.norm(vector))
    if norm == 0:
        raise ValueError("stored embedding has zero norm")
    return vector / norm


def _distance_bucket(bbox_w: int, bbox_h: int) -> str:
    """Bucket a face by the smaller side, which is what bounds identifiability.

    The identification floor is ~80-112 px (docs/hardware/pixels_per_face.md),
    so the buckets are chosen around it rather than at round numbers.
    """
    side = min(int(bbox_w), int(bbox_h))
    if side < 40:
        return "under_40px"
    if side < 64:
        return "40_63px"
    if side < 112:
        return "64_111px"
    return "112px_plus"


def collect_score_populations(
    db: Session,
    tenant_id: str,
    *,
    max_negatives_per_sighting: int = 400,
    seed: int = 0,
) -> ScorePopulations:
    """Build calibration populations from one tenant's stored evidence.

    Args:
        db: Session bound to the tenant's connection.
        tenant_id: Tenant whose gallery and events to use.
        max_negatives_per_sighting: Cap on impostor comparisons per labelled
            sighting. With 300 students x 15 exemplars that is 4475
            comparisons per sighting; sampling keeps a single session from
            producing a 100k-row report and keeps the negatives from being
            overwhelmingly one particular impostor pair.
        seed: Sampling seed, so a rerun gives the same report.

    Returns:
        A :class:`ScorePopulations`. Empty populations are returned with
        counts explaining why, rather than raising: "we have no labelled data
        yet" is the single most likely state of a fresh deployment and the
        script has to say so clearly.
    """
    from app.models.tenancy import AttendanceEvent, FaceGallery, ReviewQueueItem

    # --- Gallery, grouped by identity ----------------------------------
    gallery: dict[str, list[FloatArray]] = defaultdict(list)
    for row in db.execute(
        select(FaceGallery.roll_no, FaceGallery.embedding).where(
            FaceGallery.tenant_id == tenant_id, FaceGallery.removed_at.is_(None)
        )
    ).all():
        try:
            gallery[row.roll_no].append(_unpack(row.embedding))
        except ValueError:
            log.warning("skipping degenerate gallery vector", extra={"roll_no": row.roll_no})

    # --- Events, split by where the identity came from ------------------
    labelled_cluster_ids = set(
        db.scalars(
            select(ReviewQueueItem.cluster_id).where(
                ReviewQueueItem.tenant_id == tenant_id,
                ReviewQueueItem.resolved_roll_no.is_not(None),
            )
        ).all()
    )

    positives: list[float] = []
    negatives: list[float] = []
    by_distance: dict[str, list[float]] = defaultdict(list)
    labelled = auto = no_label = 0

    rng = np.random.default_rng(seed)
    events = db.execute(
        select(
            AttendanceEvent.roll_no,
            AttendanceEvent.embedding,
            AttendanceEvent.match_type,
            AttendanceEvent.cluster_id,
            AttendanceEvent.bbox_w,
            AttendanceEvent.bbox_h,
        ).where(
            AttendanceEvent.tenant_id == tenant_id, AttendanceEvent.embedding.is_not(None)
        )
    ).all()

    for event in events:
        is_labelled = event.match_type in HUMAN_LABELLED_MATCH_TYPES or (
            event.cluster_id is not None and event.cluster_id in labelled_cluster_ids
        )
        if not is_labelled:
            if event.roll_no is not None:
                auto += 1
            else:
                no_label += 1
            continue
        if event.roll_no is None or event.roll_no not in gallery:
            no_label += 1
            continue

        labelled += 1
        try:
            query = _unpack(event.embedding)
        except ValueError:
            continue

        for exemplar in gallery[event.roll_no]:
            score = float(np.dot(query, exemplar))
            positives.append(score)
            by_distance[_distance_bucket(event.bbox_w, event.bbox_h)].append(score)

        impostor_pool: list[FloatArray] = []
        for roll_no, exemplars in gallery.items():
            if roll_no == event.roll_no:
                continue
            impostor_pool.extend(exemplars)
        if impostor_pool and max_negatives_per_sighting > 0:
            if len(impostor_pool) > max_negatives_per_sighting:
                pick = rng.choice(
                    len(impostor_pool), size=max_negatives_per_sighting, replace=False
                )
                impostor_pool = [impostor_pool[int(i)] for i in pick]
            for exemplar in impostor_pool:
                negatives.append(float(np.dot(query, exemplar)))

    if auto:
        log.info(
            "calibration excluded %d auto-confirmed events: calibrating on the "
            "matcher's own output is circular",
            auto,
            extra={"stage": "calibration", "excluded_auto": auto},
        )

    return ScorePopulations(
        positives=tuple(positives),
        negatives=tuple(negatives),
        labelled_sightings=labelled,
        gallery_students=len(gallery),
        excluded_auto=auto,
        excluded_no_label=no_label,
        by_distance={k: tuple(v) for k, v in by_distance.items()},
    )


def calibrate_from_database(
    db: Session,
    tenant_id: str,
    *,
    far_target: float = 0.001,
    low_keep_fraction: float = 0.99,
) -> tuple[CalibrationReport, ScorePopulations]:
    """Convenience wrapper: collect populations, then calibrate."""
    populations = collect_score_populations(db, tenant_id)
    report = calibrate(
        populations.positives,
        populations.negatives,
        far_target=far_target,
        low_keep_fraction=low_keep_fraction,
    )
    return report, populations


__all__ = [
    "HUMAN_LABELLED_MATCH_TYPES",
    "ScorePopulations",
    "calibrate_from_database",
    "collect_score_populations",
]
