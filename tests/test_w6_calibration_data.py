"""Calibration from real database rows.

These tests seed an actual SQLite database with an actual gallery and actual
attendance events, because the failure this guards against is a query that
returns nothing: a calibration report computed over an empty population prints
a confident table of zeroes, and zeroes look like a result.
"""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime

import numpy as np
import pytest
from sqlalchemy.orm import Session

from app.models.database import SessionLocal
from app.services import tenancy
from app.services.calibration import calibrate_from_database, collect_score_populations


def _unit(seed: int, dim: int = 16) -> np.ndarray:
    rng = np.random.default_rng(seed)
    vector = rng.normal(size=dim).astype(np.float32)
    return vector / float(np.linalg.norm(vector))


def _person(seed: int, *, dim: int = 16, noise: float = 0.06) -> list[np.ndarray]:
    """A set of same-person vectors around a centroid."""
    base = _unit(seed, dim)
    out = []
    for i in range(8):
        vector = base + noise * np.random.default_rng(seed * 100 + i).normal(size=dim)
        out.append(vector / float(np.linalg.norm(vector)))
    return out


@pytest.fixture
def seeded(db: Session) -> tuple[str, list[str]]:
    """One tenant, four students, gallery rows and human-labelled events.

    Events are labelled ``manual_label`` -- i.e. a human said who they were --
    because that is the only population a calibration may be computed on
    without measuring the thresholds against themselves.
    """
    tenant_id = "t-calib"
    db.add(tenancy.Tenant(tenant_id=tenant_id, slug="calib", name="Calibration College"))
    db.flush()

    rolls = [f"C{i}" for i in range(1, 5)]
    for index, roll_no in enumerate(rolls):
        student = tenancy.Student(
            tenant_id=tenant_id,
            student_id=f"s-{roll_no}",
            roll_no=roll_no,
            name=f"Student {roll_no}",
        )
        db.add(student)
        db.flush()
        for vector in _person(index + 1):
            tenancy.add_gallery_entry(
                db,
                tenant_id,
                student.student_id,
                roll_no,
                vector.astype(np.float32).tobytes(),
                hashlib.sha256(vector.astype(np.float32).tobytes()).hexdigest(),
                f"crops/{tenant_id}/{roll_no}.jpg",
                "enrollment",
            )
    db.commit()

    klass = tenancy.Class(
        tenant_id=tenant_id,
        class_id="c-calib",
        code="CAL101",
        name="Calibration",
    )
    db.add(klass)
    db.flush()
    session = tenancy.create_session(db, tenant_id, klass.class_id)
    db.commit()

    now = datetime.now(UTC)
    for index, roll_no in enumerate(rolls):
        for sighting in _person(index + 1, noise=0.06)[:4]:
            db.add(
                tenancy.AttendanceEvent(
                    tenant_id=tenant_id,
                    session_id=session.session_id,
                    frame_id=f"f-{roll_no}-{sighting.tobytes()[:4].hex()}",
                    roll_no=roll_no,
                    embedding=sighting.astype(np.float32).tobytes(),
                    bbox_x=0,
                    bbox_y=0,
                    bbox_w=140,
                    bbox_h=140,
                    confidence_score=0.8,
                    # HUMAN label. Auto-confirmed rows are excluded by design.
                    match_type="manual_label",
                    captured_at=now,
                )
            )
    db.commit()
    return tenant_id, rolls


@pytest.fixture
def db() -> Session:
    session = SessionLocal()
    _truncate_tenancy_tables(session)
    yield session
    session.rollback()
    _truncate_tenancy_tables(session)
    session.close()


def _truncate_tenancy_tables(session: Session) -> None:
    """Keep committed calibration fixtures isolated on the shared test engine."""
    from app.models.database import Base

    session.rollback()
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


class TestCollectScorePopulations:
    def test_human_labelled_events_produce_both_populations(self, db: Session, seeded: object) -> None:
        tenant_id, _rolls = seeded  # type: ignore[misc]
        populations = collect_score_populations(db, tenant_id)
        assert populations.positives, "same-person pairs must be produced"
        assert populations.negatives, "impostor pairs must be produced"
        assert populations.labelled_sightings == 16
        assert populations.gallery_students == 4
        assert populations.excluded_auto == 0

    def test_impostor_pairs_outnumber_genuine_pairs(self, db: Session, seeded: object) -> None:
        """4 students x 8 exemplars x 16 sightings gives many more negatives.

        This is the mechanism that produces enough impostor comparisons for a
        meaningful FAR without collecting a classroom's worth of strangers.
        """
        tenant_id, _rolls = seeded  # type: ignore[misc]
        populations = collect_score_populations(db, tenant_id)
        assert len(populations.negatives) > len(populations.positives)

    def test_auto_confirmed_events_are_excluded(self, db: Session, seeded: object) -> None:
        """Calibrating on the matcher's own output is circular."""
        tenant_id, _rolls = seeded  # type: ignore[misc]
        tenant = tenancy.get_tenant(db, tenant_id)
        assert tenant is not None
        events = db.query(tenancy.AttendanceEvent).filter_by(tenant_id=tenant_id).all()
        events[0].match_type = "confirmed"
        db.commit()
        populations = collect_score_populations(db, tenant_id)
        assert populations.excluded_auto == 1
        assert populations.labelled_sightings == 15

    def test_similarity_of_a_seeded_person_is_high(self, db: Session, seeded: object) -> None:
        """Sanity on the maths: a re-photograph of one person scores high."""
        tenant_id, _rolls = seeded  # type: ignore[misc]
        populations = collect_score_populations(db, tenant_id)
        assert min(populations.positives) > max(populations.negatives), (
            "with clean synthetic vectors the two populations must not overlap; "
            "if they do, the scoring code is wrong, not the data"
        )
        assert min(populations.positives) > 0.85

    def test_distance_buckets_are_recorded(self, db: Session, seeded: object) -> None:
        tenant_id, _rolls = seeded  # type: ignore[misc]
        populations = collect_score_populations(db, tenant_id)
        assert "112px_plus" in populations.by_distance

    def test_empty_tenant_returns_empty_populations_with_zero_counts(self, db: Session) -> None:
        """No data is reported as zero, never as a perfect score."""
        db.add(tenancy.Tenant(tenant_id="t-empty", slug="empty", name="Empty College"))
        db.commit()
        populations = collect_score_populations(db, "t-empty")
        assert populations.positives == ()
        assert populations.negatives == ()
        assert populations.labelled_sightings == 0


class TestCalibrateFromDatabase:
    def test_separated_populations_recommend_a_usable_threshold(self, db: Session, seeded: object) -> None:
        tenant_id, _rolls = seeded  # type: ignore[misc]
        report, populations = calibrate_from_database(db, tenant_id)
        assert 0.0 < report.recommended_high <= 1.0
        assert report.recommended_low <= report.recommended_high
        assert report.kept_fraction > 0.9
        # With synthetic, cleanly separated vectors the safe threshold costs
        # almost nothing, which is what a real, separable population looks like.
        assert len(populations.positives) == report.positives

    def test_report_is_json_serialisable(self, db: Session, seeded: object) -> None:
        import json

        tenant_id, _rolls = seeded  # type: ignore[misc]
        report, populations = calibrate_from_database(db, tenant_id)
        payload = {"report": report.as_dict(), "populations": populations.as_dict()}
        assert json.loads(json.dumps(payload))["report"]["positives"] > 0
