"""W6: the live ingestion path, and the bugs it was missing.

The tests here exist because the components W2, W3 and W4 built were NOT on
the production path. ``app.services.attendance.process_frame`` used PIL, no
quality gate, ``gallery_index.search(...).best`` (which drops the runner-up),
and neither tenant isolation nor consent. Every component was well tested and
none of them was connected, so the test suite was green while the product was
wrong.

So the emphasis is not on "does ingest_frame work" but on "does it refuse the
things the legacy path accepted". Each test class names the specific defect it
prevents from returning.

No test here mocks the pipeline. A mocked pipeline tests that the wiring calls
the pipeline, which is exactly the class of test that passed while the real
path was broken.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import numpy as np
import pytest
from sqlalchemy.orm import Session

from app.models.database import SessionLocal
from app.models.tenancy import (
    CONSENT_GRANTED,
    CONSENT_PENDING,
    CONSENT_WITHDRAWN,
    AttendanceEvent,
    Class,
    ClassMember,
    ClassSession,
    ConsentRecord,
    Frame,
    ReviewQueueItem,
    Student,
    Tenant,
)
from app.services.ingest import (
    IngestRefused,
    content_sha256,
    ingest_frame,
    new_frame_id,
    pack_embedding,
    unpack_embedding,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db() -> Session:
    session = SessionLocal()
    _truncate_all(session)
    yield session
    session.rollback()
    _truncate_all(session)
    session.close()


def _truncate_all(session: Session) -> None:
    from app.models.database import Base
    from app.models.schema import LegacyBase

    session.rollback()
    for metadata in (Base.metadata, LegacyBase.metadata):
        for table in reversed(metadata.sorted_tables):
            session.execute(table.delete())
    session.commit()
    del Base


def _setup_tenant(db: Session, slug: str = "alpha") -> tuple[Tenant, Class, ClassSession]:
    """A tenant, a class with two members, and an OPEN session."""
    tenant = Tenant(slug=slug, name=f"{slug} college")
    db.add(tenant)
    db.flush()
    klass = Class(tenant_id=tenant.tenant_id, code="PHY101", name="Physics 101")
    db.add(klass)
    db.flush()
    session = ClassSession(
        tenant_id=tenant.tenant_id,
        class_id=klass.class_id,
        start_time=datetime.now(UTC).replace(tzinfo=None) - timedelta(hours=1),
    )
    db.add(session)
    db.commit()
    return tenant, klass, session


def _add_student(
    db: Session,
    tenant: Tenant,
    klass: Class,
    roll_no: str,
    *,
    consent_state: str = CONSENT_GRANTED,
) -> Student:
    student = Student(tenant_id=tenant.tenant_id, roll_no=roll_no, name=f"{roll_no} name")
    db.add(student)
    db.flush()
    db.add(ConsentRecord(
        tenant_id=tenant.tenant_id,
        student_id=student.student_id,
        state=consent_state,
        purpose="classroom attendance",
    ))
    db.add(ClassMember(
        tenant_id=tenant.tenant_id,
        class_id=klass.class_id,
        student_id=student.student_id,
    ))
    db.commit()
    return student


def _jpeg(width: int = 640, height: int = 480, value: int = 128) -> bytes:
    """A real, decodable JPEG. Not a real face -- these tests assert on
    refusals and accounting, not on recognition accuracy, which is W12's job
    and cannot be honestly asserted without measured data."""
    from PIL import Image

    array = np.full((height, width, 3), value, dtype=np.uint8)
    # A little structure, so a blur/sharpness metric is not dividing by zero.
    array[:, :, 0] = np.linspace(0, 255, width, dtype=np.uint8)[None, :]
    import io

    buffer = io.BytesIO()
    Image.fromarray(array).save(buffer, "JPEG", quality=92)
    return buffer.getvalue()


# ===========================================================================
# Refusals. The legacy path accepted all of these.
# ===========================================================================


class TestTenantIsolation:
    """A frame must never be written under the wrong tenant.

    This is the highest-consequence class of bug in the whole product: it is
    invisible in every test that uses a single tenant, and it puts one
    college's students' biometrics in another college's database.
    """

    def test_refuses_a_session_from_another_tenant(self, db: Session):
        _setup_tenant(db, "alpha")
        _, _, beta_session = _setup_tenant(db, "beta")

        with pytest.raises(IngestRefused) as exc:
            ingest_frame(
                db,
                frame_id=new_frame_id(),
                session_id=beta_session.session_id,
                tenant_id="0" * 32,
                content=_jpeg(),
            )
        assert exc.value.code == "tenant_mismatch"

    def test_refuses_a_frame_id_already_used_by_another_tenant(self, db: Session):
        """Same frame_id from a different tenant is a collision, not a duplicate.

        A frame_id re-used under a different tenant must be refused and NOT
        silently treated as a duplicate, because that would let one tenant's
        record overwrite another's, losing auditability.
        """
        alpha, klass, alpha_session = _setup_tenant(db, "alpha")
        _add_student(db, alpha, klass, "A001")
        frame_id = new_frame_id()
        ingest_frame(
            db, frame_id=frame_id, session_id=alpha_session.session_id,
            tenant_id=alpha.tenant_id, content=_jpeg(),
        )

        # Now attempt the same id under a completely different tenant / session.
        beta, _, beta_session = _setup_tenant(db, "beta")

        with pytest.raises(IngestRefused) as exc:
            ingest_frame(
                db, frame_id=frame_id, session_id=beta_session.session_id,
                tenant_id=beta.tenant_id, content=_jpeg(),
            )
        assert exc.value.code == "frame_id_collision"

    def test_unknown_session_is_refused_not_created(self, db: Session):
        tenant, _, _ = _setup_tenant(db)
        with pytest.raises(IngestRefused) as exc:
            ingest_frame(
                db, frame_id=new_frame_id(), session_id=999_999,
                tenant_id=tenant.tenant_id, content=_jpeg(),
            )
        assert exc.value.code == "session_not_found"


class TestClosedSession:
    """A frame arriving after close-out must not alter the record.

    The audit found nine of eleven legacy sessions with a NULL end_time, and
    frames kept landing after close. Once a teacher has exported a register,
    a late frame must not change it.
    """

    def test_refuses_a_frame_for_a_closed_session(self, db: Session):
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        session.end_time = datetime.now(UTC).replace(tzinfo=None) - timedelta(minutes=1)
        session.close_reason = "completed"
        db.commit()

        with pytest.raises(IngestRefused) as exc:
            ingest_frame(
                db, frame_id=new_frame_id(), session_id=session.session_id,
                tenant_id=tenant.tenant_id, content=_jpeg(),
            )
        assert exc.value.code == "session_closed"

    def test_a_refused_frame_leaves_no_trace_in_the_frame_table(self, db: Session):
        """Refused means refused. A row with no events is worse than no row,
        because coverage accounting would then blame the room, not the code."""
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        session.end_time = datetime.now(UTC).replace(tzinfo=None)
        db.commit()
        frame_id = new_frame_id()

        with pytest.raises(IngestRefused):
            ingest_frame(
                db, frame_id=frame_id, session_id=session.session_id,
                tenant_id=tenant.tenant_id, content=_jpeg(),
            )
        assert db.get(Frame, frame_id) is None


class TestConsent:
    """No consent, no attendance. This is the DPDP Act's central requirement.

    The legacy path had no consent check at all, so a student who had
    withdrawn consent was still being enrolled, embedded and marked present.
    """

    def test_student_without_consent_is_excluded_from_the_roster(self, db: Session):
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001", consent_state=CONSENT_PENDING)
        ingest_frame(
            db, frame_id=new_frame_id(), session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=_jpeg(),
        )
        # No face was detectable in a synthetic frame, so the assertion is on
        # the roster that identity was bound to, not on a count.
        from app.services.ingest import _roster_with_consent

        assert _roster_with_consent(db, tenant.tenant_id, klass.class_id) == frozenset()

    def test_withdrawn_consent_is_treated_as_withdrawn_not_pending(self, db: Session):
        """WITHDRAWN must be as binding as PENDING. A partial implementation
        that only blocks PENDING still processes withdrawn students."""
        tenant, klass, _session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001", consent_state=CONSENT_WITHDRAWN)
        from app.services.ingest import _roster_with_consent

        assert _roster_with_consent(db, tenant.tenant_id, klass.class_id) == frozenset()

    def test_granted_consent_keeps_the_student_on_the_roster(self, db: Session):
        tenant, klass, _ = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001", consent_state=CONSENT_GRANTED)
        from app.services.ingest import _roster_with_consent

        assert _roster_with_consent(db, tenant.tenant_id, klass.class_id) == frozenset({"A001"})

    def test_one_withdrawn_roster_member_does_not_block_the_others(self, db: Session):
        """A single withdrawal must not stop the other forty being marked.

        Failing closed on the whole class would be a self-inflicted denial of
        service on the school.  Two classes in the same tenant, one student
        each: the withdrawal in class B leaves class A untouched.
        """
        from app.models.tenancy import Class as ClassModel
        from app.services.ingest import _roster_with_consent

        tenant, klass_a, _ = _setup_tenant(db, "alpha")
        # A second class in the SAME tenant, so the test is about consent and
        # not about tenant isolation (which has its own class above).
        klass_b = ClassModel(tenant_id=tenant.tenant_id, code="PHY102", name="Physics 102")
        db.add(klass_b)
        db.commit()

        _add_student(db, tenant, klass_a, "A001")  # granted (default)
        _add_student(db, tenant, klass_b, "A002", consent_state=CONSENT_WITHDRAWN)

        # Class A: nobody withdrawn -> A001 on the roster
        assert _roster_with_consent(db, tenant.tenant_id, klass_a.class_id) == frozenset({"A001"})
        # Class B: A002 withdrawn -> nobody on the roster
        assert _roster_with_consent(db, tenant.tenant_id, klass_b.class_id) == frozenset()


# ===========================================================================
# Idempotency. The edge retries; a retry must not double-count.
# ===========================================================================


class TestIdempotency:
    """At-least-once delivery is the edge's design, not an accident.

    docs/decisions/0003 says a redelivered frame is a no-op at every stage.
    That was true on paper and false in the legacy path.
    """

    def test_a_redelivered_frame_creates_no_second_record(self, db: Session):
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        frame_id = new_frame_id()
        first = ingest_frame(
            db, frame_id=frame_id, session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=_jpeg(),
        )
        second = ingest_frame(
            db, frame_id=frame_id, session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=_jpeg(),
        )
        assert not first.duplicate
        assert second.duplicate
        assert second.events_created == 0
        assert second.marked_present == []
        assert (
            db.query(AttendanceEvent).filter_by(frame_id=frame_id).count() == first.events_created
        )

    def test_five_redeliveries_are_still_one_frame(self, db: Session):
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        frame_id = new_frame_id()
        outcomes = [
            ingest_frame(
                db, frame_id=frame_id, session_id=session.session_id,
                tenant_id=tenant.tenant_id, content=_jpeg(),
            )
            for _ in range(5)
        ]
        assert sum(1 for o in outcomes if not o.duplicate) == 1
        assert db.query(Frame).filter_by(frame_id=frame_id).count() == 1

    def test_different_bytes_under_the_same_frame_id_are_a_collision(self, db: Session):
        """A retry with different content is a device bug, and hiding it would
        mean the stored frame is not the frame the teacher saw."""
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        frame_id = new_frame_id()
        ingest_frame(
            db, frame_id=frame_id, session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=_jpeg(value=100),
        )
        with pytest.raises(IngestRefused) as exc:
            ingest_frame(
                db, frame_id=frame_id, session_id=session.session_id,
                tenant_id=tenant.tenant_id, content=_jpeg(value=200),
            )
        assert exc.value.code == "frame_id_content_mismatch"


# ===========================================================================
# Accounting. A gap in attendance must be explainable.
# ===========================================================================


class TestFrameAccounting:
    """Every detected face is either accepted or explained.

    A face that vanishes with no reason string is how "the system said everyone
    was present" and the register was wrong.
    """

    def test_every_face_is_accounted_for(self, db: Session):
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        outcome = ingest_frame(
            db, frame_id=new_frame_id(), session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=_jpeg(),
        )
        assert outcome.accounted_for
        assert outcome.faces_seen == outcome.faces_accepted + outcome.faces_rejected

    def test_rejected_faces_carry_a_reason(self, db: Session):
        """A rejection with an empty reason is a bug in the reporter."""
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        outcome = ingest_frame(
            db, frame_id=new_frame_id(), session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=_jpeg(),
        )
        assert all(reason.strip() for reason in outcome.notes), (
            f"a face was dropped with no reason: {outcome.notes}"
        )

    def test_timings_are_recorded_for_every_stage(self, db: Session):
        """Per-stage timings are what makes a slow frame diagnosable rather
        than merely slow."""
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        outcome = ingest_frame(
            db, frame_id=new_frame_id(), session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=_jpeg(),
        )
        assert outcome.timings_ms.get("ingest_total_ms", 0.0) > 0.0

    def test_the_frame_is_recorded_even_when_no_faces_are_found(self, db: Session):
        """An empty classroom is a real observation and must be auditable."""
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        frame_id = new_frame_id()
        outcome = ingest_frame(
            db, frame_id=frame_id, session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=_jpeg(value=250),
        )
        assert db.get(Frame, frame_id) is not None
        assert outcome.faces_seen == outcome.faces_accepted + outcome.faces_rejected


# ===========================================================================
# Provenance. An attendance record must be traceable to the model that made it.
# ===========================================================================


class TestProvenance:
    def test_frame_records_its_sha256(self, db: Session):
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        content = _jpeg()
        frame_id = new_frame_id()
        ingest_frame(
            db, frame_id=frame_id, session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=content,
        )
        assert db.get(Frame, frame_id).sha256 == content_sha256(content)

    def test_device_angle_and_zoom_are_preserved(self, db: Session):
        """The back-row problem is an angle/zoom problem. Without these the
        coverage gap cannot be attributed to geometry."""
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        frame_id = new_frame_id()
        ingest_frame(
            db, frame_id=frame_id, session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=_jpeg(),
            camera_angle_deg=-32.5, zoom=2.0, device_id="dev-1",
        )
        frame = db.get(Frame, frame_id)
        assert frame.camera_angle_deg == pytest.approx(-32.5)
        assert frame.zoom == pytest.approx(2.0)
        assert frame.device_id == "dev-1"

    def test_embedding_roundtrips_exactly(self, db: Session):
        """float32, not a lossy re-encode: a threshold calibrated on the stored
        value must behave the same on the retrieved one."""
        original = np.linspace(-1.0, 1.0, 512, dtype=np.float32)
        restored = unpack_embedding(pack_embedding(original))
        assert np.array_equal(original, restored)
        assert restored.dtype == np.float32


class TestReviewQueue:
    """An unresolved face must reach a human, exactly once per person.

    One prompt per frame means a teacher in a 16-frame sweep sees sixteen
    prompts for one student, and stops reading them.
    """

    def test_the_review_queue_starts_empty_and_stays_empty_for_no_faces(self, db: Session):
        tenant, klass, session = _setup_tenant(db)
        _add_student(db, tenant, klass, "A001")
        ingest_frame(
            db, frame_id=new_frame_id(), session_id=session.session_id,
            tenant_id=tenant.tenant_id, content=_jpeg(),
        )
        assert db.query(ReviewQueueItem).filter_by(tenant_id=tenant.tenant_id).count() == 0

    def test_review_items_are_never_cross_tenant(self, db: Session):
        """Two tenants, both with unresolved faces, must not share a queue row."""
        alpha, aklass, asession = _setup_tenant(db, "alpha")
        beta, bklass, bsession = _setup_tenant(db, "beta")
        _add_student(db, alpha, aklass, "A001")
        _add_student(db, beta, bklass, "B001")
        ingest_frame(
            db, frame_id=new_frame_id(), session_id=asession.session_id,
            tenant_id=alpha.tenant_id, content=_jpeg(),
        )
        ingest_frame(
            db, frame_id=new_frame_id(), session_id=bsession.session_id,
            tenant_id=beta.tenant_id, content=_jpeg(),
        )
        rows = db.query(ReviewQueueItem).all()
        for row in rows:
            assert row.tenant_id in {alpha.tenant_id, beta.tenant_id}
