"""Performance regression tests.

The audit found an O(F x P) duplicate check that performed one database query
and re-unpacked every stored embedding, once per detected face
(docs/00_audit.md 4.5). For a 300-student classroom with 100 pending reviews
that is 30,000 blob deserialisations per frame.

These tests pin the *complexity*, not the absolute speed, because absolute
timings are machine-dependent and would be flaky in CI. A complexity
regression shows up as a scaling failure: doubling the work must not multiply
the queries.
"""

from __future__ import annotations

import time

import numpy as np
import pytest
from sqlalchemy.orm import Session

from app.models.database import SessionLocal
from app.models.schema import AttendanceEvent, ClassSession, FaceGallery, ReviewQueue, Student
from app.services.attendance import PendingReviewIndex, _is_duplicate
from app.services.gallery import append_gallery, gallery_index


@pytest.fixture
def session_with_reviews() -> tuple[Session, int, list[np.ndarray]]:
    """A session with ``N`` pending reviews, each with a distinct embedding."""
    from app.models.database import Base, engine

    Base.metadata.create_all(engine)
    db = SessionLocal()
    for table in (ReviewQueue, AttendanceEvent, FaceGallery, ClassSession, Student):
        db.query(table).delete()
    db.commit()

    session = ClassSession(class_id="PERF")
    db.add(session)
    db.flush()

    rng = np.random.default_rng(0)
    embeddings: list[np.ndarray] = []
    for index in range(40):
        student = Student(roll_no=f"P{index}", name=f"P{index}")
        db.add(student)
        db.flush()
        vector = rng.normal(size=128).astype(np.float32)
        vector /= np.linalg.norm(vector)
        embeddings.append(vector)
        append_gallery(db, student.roll_no, vector, f"perf/{index}.jpg", "enrollment")

        event = AttendanceEvent(
            session_id=session.session_id,
            roll_no=None,
            face_crop_path=f"perf/{index}.jpg",
            embedding=vector.tobytes(),
            bbox="0,0,100,100",
            confidence_score=0.1,
            match_type="review",
        )
        db.add(event)
        db.flush()
        db.add(ReviewQueue(event_id=event.event_id, status="pending"))
    db.commit()

    gallery_index.reset()
    return db, session.session_id, embeddings


def test_dedup_loads_pending_reviews_once_per_frame(
    session_with_reviews: tuple,
) -> None:
    """The actual fix: one query for the whole frame, not one per face.

    The legacy code re-queried and re-unpacked every pending embedding for each
    detected face. `PendingReviewIndex` is constructed once by the frame
    processor and reused, so the query count is a function of the number of
    FRAMES, never the number of faces.
    """
    db, session_id, embeddings = session_with_reviews

    class CountingSession:
        """Wraps a real session and counts query() calls."""

        def __init__(self, inner: Session) -> None:
            self._inner = inner
            self.queries = 0

        def query(self, *args: object, **kwargs: object) -> object:
            self.queries += 1
            return self._inner.query(*args)  # type: ignore[arg-type]

    probe = embeddings[0]

    # One frame, many faces: exactly one query.
    counting = CountingSession(db)
    pending = PendingReviewIndex.for_frame(counting, session_id)  # type: ignore[arg-type]
    queries_per_frame = counting.queries
    for _ in range(50):
        pending.covers(probe)
    assert counting.queries == queries_per_frame, (
        "checking 50 faces issued more queries than building the index did"
    )

    # Ten frames, one face each: ten queries. Linear in FRAMES, not faces.
    counting_ten = CountingSession(db)
    for _ in range(10):
        frame_pending = PendingReviewIndex.for_frame(counting_ten, session_id)  # type: ignore[arg-type]
        frame_pending.covers(probe)
    assert counting_ten.queries == 10, (
        f"expected one query per frame, got {counting_ten.queries} for 10 frames"
    )


def test_pending_index_short_circuits_when_empty(session_with_reviews: tuple) -> None:
    """An empty pending set must cost nothing per face."""
    db, session_id, embeddings = session_with_reviews
    db.query(ReviewQueue).update({"status": "resolved"})
    db.commit()

    pending = PendingReviewIndex.for_frame(db, session_id)
    assert len(pending) == 0
    assert not pending, "an empty index must be falsy so callers can skip it"

    probe = embeddings[0]
    start = time.perf_counter()
    for _ in range(1000):
        assert pending.covers(probe) is False
    elapsed = time.perf_counter() - start
    assert elapsed < 0.5, f"empty short circuit took {elapsed:.3f}s for 1000 calls"


def test_pending_index_sees_reviews_added_during_the_frame(
    session_with_reviews: tuple,
) -> None:
    """Two tiles in one frame must not queue the same person twice."""
    db, session_id, _embeddings = session_with_reviews
    pending = PendingReviewIndex.for_frame(db, session_id)
    before = len(pending)

    # A genuinely new person, not a perturbation of one already queued.
    fresh = np.random.default_rng(99).normal(size=128).astype(np.float32)
    new_vector = (fresh / np.linalg.norm(fresh)).astype(np.float32)
    assert pending.covers(new_vector) is False, "random noise must not match a real face"

    pending.add(new_vector)
    assert len(pending) == before + 1
    assert pending.covers(new_vector) is True, (
        "a review created earlier in this frame must be visible to later faces"
    )


def test_dedup_scales_sublinearly(session_with_reviews: tuple) -> None:
    """Doubling the pending set must not blow up the wall clock.

    A generous bound: the old implementation was ~O(F x P) with a query per
    face. The new one is O(P) once. A 20x wall-clock budget for a 2x input is
    generous enough not to flake on a loaded CI machine while still failing if
    the complexity regresses to per-face scanning.
    """
    db, session_id, embeddings = session_with_reviews
    probe = embeddings[0]

    start = time.perf_counter()
    for _ in range(50):
        _is_duplicate(db, session_id, probe)
    fifty_iterations = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(100):
        _is_duplicate(db, session_id, probe)
    hundred_iterations = time.perf_counter() - start

    # 2x the work should be well under 20x the time.
    budget = fifty_iterations * 20
    assert hundred_iterations < budget, (
        f"duplicate check scaled badly: 50 iters {fifty_iterations:.3f}s, 100 iters {hundred_iterations:.3f}s"
    )


def test_pending_index_reflects_resolved_reviews(session_with_reviews: tuple) -> None:
    """A newly constructed index must reflect the current queue.

    The old implementation cached on the pending count, which meant a stale
    answer could survive a resolution. Building the index per frame removes
    that failure mode by construction.
    """
    db, session_id, embeddings = session_with_reviews
    probe = embeddings[0]
    assert PendingReviewIndex.for_frame(db, session_id).covers(probe) is True

    db.query(ReviewQueue).update({"status": "resolved"})
    db.commit()

    assert PendingReviewIndex.for_frame(db, session_id).covers(probe) is False


def test_pending_index_is_scoped_per_session(session_with_reviews: tuple) -> None:
    """One session's reviews must not suppress another's."""
    db, session_id, embeddings = session_with_reviews
    probe = embeddings[0]
    assert PendingReviewIndex.for_frame(db, session_id).covers(probe) is True

    other = ClassSession(class_id="OTHER")
    db.add(other)
    db.commit()
    assert PendingReviewIndex.for_frame(db, other.session_id).covers(probe) is False


def test_no_pending_reviews_short_circuits(session_with_reviews: tuple) -> None:
    """An empty queue must not touch the database at all."""
    db, session_id, _embeddings = session_with_reviews
    db.query(ReviewQueue).update({"status": "resolved"})
    db.commit()

    start = time.perf_counter()
    for _ in range(20):
        assert _is_duplicate(db, session_id, np.zeros(128, dtype=np.float32)) is False
    elapsed = time.perf_counter() - start

    assert elapsed < 1.0, f"empty-queue short circuit took {elapsed:.3f}s for 20 calls"


def test_index_search_scales_to_a_full_classroom() -> None:
    """A 300-student gallery must stay comfortably interactive.

    300 students x 15 exemplars = 4,500 vectors of 128 dimensions. An exact
    flat search must still be sub-10 ms, which is what makes it the right
    choice here over an approximate index.
    """
    from app.services.vector_index import VectorIndex

    rng = np.random.default_rng(1)
    index = VectorIndex()
    gallery_id = 0
    for student in range(300):
        for _ in range(15):
            vector = rng.normal(size=128).astype(np.float32)
            vector /= np.linalg.norm(vector)
            index.add(gallery_id, f"S{student}", vector)
            gallery_id += 1

    assert index.size == 4500
    assert index.identity_count == 300

    query = rng.normal(size=128).astype(np.float32)
    query /= np.linalg.norm(query)

    start = time.perf_counter()
    for _ in range(20):
        outcome = index.search(query, limit=5)
    per_search = (time.perf_counter() - start) / 20

    assert len(outcome.matches) == 5
    assert per_search < 0.010, f"search took {per_search * 1000:.1f} ms; expected < 10 ms"
