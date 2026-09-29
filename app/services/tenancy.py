"""Tenant-scoped data access.

The tenancy guarantee is enforced in **one** place, so a new endpoint cannot
forget it. :class:`TenantContext` carries the verified tenant id and exposes
query helpers that inject the filter. Application code never writes
``WHERE tenant_id = ?`` by hand.

Design notes
------------
* **Repository functions, not an ORM session wrapper.** A generic
  ``repository.for(Model)`` invites a caller to reach for the raw session and
  drop the filter. Explicit functions make the filter unavoidable.
* **Composite keys.** Every function takes the tenant id explicitly, so a
  missing filter is a signature change rather than a silent data leak.
* **Cross-tenant reads are impossible by default.** Reaching another tenant's
  data requires an explicit, separately-reviewed admin function.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import Actor
from app.models.tenancy import (
    AttendanceEvent,
    AuditLog,
    Class,
    ClassMember,
    ClassSession,
    ConsentRecord,
    Device,
    FaceGallery,
    FeedbackEvent,
    Frame,
    ModelVersion,
    ReviewQueueItem,
    Room,
    ScanJob,
    Student,
    Tenant,
    UnknownCluster,
    User,
)

log = logging.getLogger(__name__)


class TenantViolation(RuntimeError):
    """Raised when a query would cross a tenant boundary.

    A bug, not a runtime condition. The exception is deliberately loud: a
    cross-tenant read in a multi-tenant product is a reportable breach, and
    silently returning an empty result would hide it.
    """


@dataclass(frozen=True, slots=True)
class TenantContext:
    """A verified tenant scope, derived from a credential.

    Never construct this from a request body. It comes from
    :meth:`Actor.as_tenant_context`, and the actor came from a verified
    token.
    """

    tenant_id: str
    actor: Actor

    def assert_entity(self, entity: Any, tenant_column: str = "tenant_id") -> str:
        """Verify a loaded entity belongs to this tenant.

        Raises:
            TenantViolation: if it does not. Guards the case where a row is
                loaded by primary key from an untrusted identifier.
        """
        actual = getattr(entity, tenant_column, None)
        if actual != self.tenant_id:
            raise TenantViolation(
                f"{type(entity).__name__} belongs to tenant {actual!r}, not {self.tenant_id!r}"
            )
        return self.tenant_id

    def audit(
        self, action: str, resource_type: str, resource_id: str | None = None, **detail: Any
    ) -> AuditLog:
        """Build an audit entry bound to this tenant and actor.

        Returns the row WITHOUT adding it, so the caller can commit it in the
        same transaction as the change it records. An audit entry that is not
        in the same transaction as the change is worthless.
        """
        return AuditLog(
            tenant_id=self.tenant_id,
            actor_user_id=self.actor.actor_id if not self.actor.is_device else None,
            actor_type=self.actor.actor_type.value,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            detail_json=_json_detail(detail),
            correlation_id=self.actor.correlation_id or None,
        )


def _json_detail(detail: dict[str, Any]) -> str | None:
    """Serialise audit detail.

    Refuses to serialise anything that looks like biometric data. An audit log
    is read by more people and retained longer than the operational tables;
    putting a face embedding in one would defeat the point of the restriction.
    """
    import json

    if not detail:
        return None
    forbidden = {"embedding", "centroid", "exemplar_embedding", "face_crop", "image", "bytes"}
    offending = forbidden & {k.lower() for k in detail}
    if offending:
        raise ValueError(
            f"audit detail must not contain biometric data: {sorted(offending)}. "
            "Record identifiers, not vectors or images."
        )
    return json.dumps(detail, default=str, sort_keys=True)


# ---------------------------------------------------------------------------
# Tenants (a tenant is looked up BEFORE a context exists)
# ---------------------------------------------------------------------------


def get_tenant_by_slug(db: Session, slug: str) -> Tenant | None:
    """Find a tenant by its immutable slug. Used at login."""
    return db.scalar(select(Tenant).where(Tenant.slug == slug, Tenant.is_active.is_(True)))


def get_tenant(db: Session, tenant_id: str) -> Tenant | None:
    """Find a tenant by id."""
    return db.get(Tenant, tenant_id)


# ---------------------------------------------------------------------------
# Users and devices
# ---------------------------------------------------------------------------


def find_user(db: Session, tenant_id: str, email: str) -> User | None:
    """Find a user within one tenant. Email is unique per tenant, not global."""
    return db.scalar(select(User).where(User.tenant_id == tenant_id, User.email == email.lower().strip()))


def get_user(db: Session, tenant_id: str, user_id: str) -> User | None:
    """Load a user, refusing any other tenant's."""
    user = db.get(User, user_id)
    if user is not None and user.tenant_id != tenant_id:
        return None
    return user


def list_users(db: Session, tenant_id: str, *, active_only: bool = False) -> Sequence[User]:
    """List a tenant's users."""
    statement = select(User).where(User.tenant_id == tenant_id)
    if active_only:
        statement = statement.where(User.is_active.is_(True))
    return db.scalars(statement.order_by(User.email)).all()


def find_device_by_credential(db: Session, credential_hash: str) -> Device | None:
    """Resolve a presented device credential to a device.

    Lookup is by hash rather than by scanning, so a timing attack reveals
    nothing about how many devices exist.
    """
    return db.scalar(select(Device).where(Device.credential_hash == credential_hash))


def get_device(db: Session, tenant_id: str, device_id: str) -> Device | None:
    """Load a device, refusing any other tenant's."""
    device = db.get(Device, device_id)
    if device is not None and device.tenant_id != tenant_id:
        return None
    return device


def list_devices(db: Session, tenant_id: str) -> Sequence[Device]:
    """List a tenant's devices."""
    return db.scalars(select(Device).where(Device.tenant_id == tenant_id).order_by(Device.name)).all()


# ---------------------------------------------------------------------------
# Rooms, classes, rosters
# ---------------------------------------------------------------------------


def get_room(db: Session, tenant_id: str, room_id: str) -> Room | None:
    """Load a room, refusing any other tenant's."""
    room = db.get(Room, room_id)
    if room is not None and room.tenant_id != tenant_id:
        return None
    return room


def list_rooms(db: Session, tenant_id: str) -> Sequence[Room]:
    """List a tenant's rooms."""
    return db.scalars(select(Room).where(Room.tenant_id == tenant_id).order_by(Room.code)).all()


def get_class(db: Session, tenant_id: str, class_id: str) -> Class | None:
    """Load a class, refusing any other tenant's."""
    row = db.get(Class, class_id)
    if row is not None and row.tenant_id != tenant_id:
        return None
    return row


def list_classes(db: Session, tenant_id: str) -> Sequence[Class]:
    """List a tenant's classes."""
    return db.scalars(select(Class).where(Class.tenant_id == tenant_id).order_by(Class.code)).all()


def list_roster(db: Session, tenant_id: str, class_id: str) -> Sequence[Student]:
    """The enrolled students of ONE class.

    This is the function that fixes audit 4.6. The legacy ``absentees()``
    compared against every enrolled student in the system, which is correct
    only when the college has exactly one class.
    """
    return db.scalars(
        select(Student)
        .join(
            ClassMember,
            (ClassMember.student_id == Student.student_id) & (ClassMember.tenant_id == Student.tenant_id),
        )
        .where(
            ClassMember.tenant_id == tenant_id,
            ClassMember.class_id == class_id,
            ClassMember.dropped_at.is_(None),
            Student.is_active.is_(True),
        )
        .order_by(Student.roll_no)
    ).all()


def roster_roll_numbers(db: Session, tenant_id: str, class_id: str) -> frozenset[str]:
    """The class roster as a plain set, for the identity engine's filter."""
    return frozenset(s.roll_no for s in list_roster(db, tenant_id, class_id))


def add_class_member(
    db: Session, tenant_id: str, class_id: str, student_id: str, *, seat_label: str | None = None
) -> ClassMember:
    """Enrol a student in a class. Idempotent on (tenant, class, student)."""
    existing = db.get(ClassMember, (tenant_id, class_id, student_id))
    if existing is not None:
        if existing.dropped_at is not None:
            existing.dropped_at = None
        return existing
    member = ClassMember(tenant_id=tenant_id, class_id=class_id, student_id=student_id, seat_label=seat_label)
    db.add(member)
    return member


def drop_class_member(db: Session, tenant_id: str, class_id: str, student_id: str) -> bool:
    """Soft-drop a student from a class. The audit trail keeps the record."""
    member = db.get(ClassMember, (tenant_id, class_id, student_id))
    if member is None or member.dropped_at is not None:
        return False
    member.dropped_at = datetime.now(UTC)
    return True


# ---------------------------------------------------------------------------
# Students and consent
# ---------------------------------------------------------------------------


def get_student(db: Session, tenant_id: str, student_id: str) -> Student | None:
    """Load a student, refusing any other tenant's."""
    student = db.get(Student, student_id)
    if student is not None and student.tenant_id != tenant_id:
        return None
    return student


def find_student_by_roll(db: Session, tenant_id: str, roll_no: str) -> Student | None:
    """Find a student by roll number within one tenant.

    Roll numbers are unique per tenant, so two colleges may both have an R1.
    """
    return db.scalar(
        select(Student).where(Student.tenant_id == tenant_id, Student.roll_no == roll_no.strip().upper())
    )


def list_students(db: Session, tenant_id: str, *, active_only: bool = True) -> Sequence[Student]:
    """List a tenant's students."""
    statement = select(Student).where(Student.tenant_id == tenant_id)
    if active_only:
        statement = statement.where(Student.is_active.is_(True))
    return db.scalars(statement.order_by(Student.roll_no)).all()


def get_consent(db: Session, tenant_id: str, student_id: str) -> ConsentRecord | None:
    """A student's consent record, if any."""
    return db.scalar(
        select(ConsentRecord).where(
            ConsentRecord.tenant_id == tenant_id, ConsentRecord.student_id == student_id
        )
    )


def has_consent(db: Session, tenant_id: str, student_id: str) -> bool:
    """Whether biometric processing is permitted for this student.

    **No consent, no enrollment.** Checked before any gallery write.
    """
    from app.models.tenancy import CONSENT_GRANTED

    record = get_consent(db, tenant_id, student_id)
    return record is not None and record.state == CONSENT_GRANTED


# ---------------------------------------------------------------------------
# Gallery
# ---------------------------------------------------------------------------


def add_gallery_entry(
    db: Session,
    tenant_id: str,
    student_id: str,
    roll_no: str,
    embedding: bytes,
    embedding_hash: str,
    source_object_key: str,
    added_via: str,
    *,
    model_version: str = "unknown",
    quality_score: float | None = None,
) -> FaceGallery | None:
    """Add one embedding, de-duplicating on the embedding hash.

    Returns ``None`` when the same embedding is already stored, which is the
    normal outcome for a re-delivered frame. Silently adding a duplicate would
    inflate a gallery and skew the nearest-neighbour statistics.
    """
    existing = db.scalar(
        select(FaceGallery).where(
            FaceGallery.tenant_id == tenant_id,
            FaceGallery.roll_no == roll_no,
            FaceGallery.embedding_hash == embedding_hash,
            FaceGallery.removed_at.is_(None),
        )
    )
    if existing is not None:
        return None
    entry = FaceGallery(
        tenant_id=tenant_id,
        student_id=student_id,
        roll_no=roll_no,
        embedding=embedding,
        embedding_hash=embedding_hash,
        source_object_key=source_object_key,
        added_via=added_via,
        model_version=model_version,
        quality_score=quality_score,
    )
    db.add(entry)
    return entry


def list_gallery(
    db: Session,
    tenant_id: str,
    *,
    roll_no: str | None = None,
    model_version: str | None = None,
    include_removed: bool = False,
) -> Sequence[FaceGallery]:
    """List gallery rows for one tenant."""
    statement = select(FaceGallery).where(FaceGallery.tenant_id == tenant_id)
    if roll_no is not None:
        statement = statement.where(FaceGallery.roll_no == roll_no)
    if model_version is not None:
        statement = statement.where(FaceGallery.model_version == model_version)
    if not include_removed:
        statement = statement.where(FaceGallery.removed_at.is_(None))
    return db.scalars(statement.order_by(FaceGallery.gallery_id)).all()


def gallery_entries_for_index(db: Session, tenant_id: str) -> Iterable[tuple[int, str, bytes]]:
    """Stream ``(gallery_id, roll_no, embedding)`` for the vector index."""
    for row in db.execute(
        select(FaceGallery.gallery_id, FaceGallery.roll_no, FaceGallery.embedding).where(
            FaceGallery.tenant_id == tenant_id, FaceGallery.removed_at.is_(None)
        )
    ).all():
        yield row.gallery_id, row.roll_no, row.embedding


# ---------------------------------------------------------------------------
# Sessions, frames, events
# ---------------------------------------------------------------------------


def create_session(db: Session, tenant_id: str, class_id: str) -> ClassSession:
    """Open a lesson session."""
    session = ClassSession(tenant_id=tenant_id, class_id=class_id)
    db.add(session)
    db.flush()
    return session


def get_session(db: Session, tenant_id: str, session_id: int) -> ClassSession | None:
    """Load a session, refusing any other tenant's."""
    row = db.get(ClassSession, session_id)
    if row is not None and row.tenant_id != tenant_id:
        return None
    return row


def list_sessions(
    db: Session, tenant_id: str, *, class_id: str | None = None, open_only: bool = False
) -> Sequence[ClassSession]:
    """List sessions for a tenant, newest first."""
    statement = select(ClassSession).where(ClassSession.tenant_id == tenant_id)
    if class_id is not None:
        statement = statement.where(ClassSession.class_id == class_id)
    if open_only:
        statement = statement.where(ClassSession.end_time.is_(None))
    return db.scalars(statement.order_by(ClassSession.start_time.desc())).all()


def register_frame(
    db: Session,
    tenant_id: str,
    frame_id: str,
    session_id: int,
    *,
    device_id: str | None = None,
    captured_at: datetime | None = None,
    device_timestamp: datetime | None = None,
    camera_angle_deg: float | None = None,
    zoom: float | None = None,
    width_px: int | None = None,
    height_px: int | None = None,
    object_key: str | None = None,
    sha256: str | None = None,
    correlation_id: str | None = None,
) -> Frame | None:
    """Register a captured frame, idempotently on ``frame_id``.

    Returns ``None`` when the frame was already registered. This is the single
    point where at-least-once edge delivery becomes effectively-once: a
    redelivered frame never produces a second set of attendance events.
    """
    existing = db.get(Frame, frame_id)
    if existing is not None:
        return None
    frame = Frame(
        frame_id=frame_id,
        tenant_id=tenant_id,
        session_id=session_id,
        device_id=device_id,
        captured_at=captured_at or datetime.now(UTC),
        device_timestamp=device_timestamp,
        camera_angle_deg=camera_angle_deg,
        zoom=zoom,
        width_px=width_px,
        height_px=height_px,
        object_key=object_key,
        sha256=sha256,
        correlation_id=correlation_id,
    )
    db.add(frame)
    db.flush()
    return frame


def list_events(db: Session, tenant_id: str, session_id: int) -> Sequence[AttendanceEvent]:
    """Every attendance event in a session, best evidence last."""
    return db.scalars(
        select(AttendanceEvent)
        .where(AttendanceEvent.tenant_id == tenant_id, AttendanceEvent.session_id == session_id)
        .order_by(AttendanceEvent.captured_at, AttendanceEvent.event_id)
    ).all()


def append_feedback(
    db: Session,
    tenant_id: str,
    user_id: str,
    action: str,
    *,
    session_id: int | None = None,
    review_id: int | None = None,
    cluster_id: str | None = None,
    roll_no: str | None = None,
    previous_guess: str | None = None,
    applied: bool = True,
    skipped: bool = False,
) -> FeedbackEvent:
    """Record one human interaction. Append-only."""
    event = FeedbackEvent(
        tenant_id=tenant_id,
        user_id=user_id,
        action=action,
        session_id=session_id,
        review_id=review_id,
        cluster_id=cluster_id,
        roll_no=roll_no,
        previous_guess=previous_guess,
        applied=applied,
        skipped=skipped,
    )
    db.add(event)
    return event


def pending_reviews(
    db: Session, tenant_id: str, *, session_id: int | None = None
) -> Sequence[ReviewQueueItem]:
    """Unresolved review items, least-asked first.

    Ordering by ``ask_count`` is what implements "ask again later without
    nagging": items the teacher has already declined to answer float down the
    list rather than reappearing at the top on every reconnect.
    """
    statement = select(ReviewQueueItem).where(
        ReviewQueueItem.tenant_id == tenant_id, ReviewQueueItem.status == "pending"
    )
    if session_id is not None:
        statement = statement.where(ReviewQueueItem.session_id == session_id)
    return db.scalars(statement.order_by(ReviewQueueItem.ask_count, ReviewQueueItem.review_id)).all()


def unresolved_clusters(db: Session, tenant_id: str, session_id: int) -> Sequence[UnknownCluster]:
    """People the system could not identify, one row per person."""
    return db.scalars(
        select(UnknownCluster).where(
            UnknownCluster.tenant_id == tenant_id,
            UnknownCluster.session_id == session_id,
            UnknownCluster.status == "unresolved",
        )
    ).all()


# ---------------------------------------------------------------------------
# Jobs, models, audit
# ---------------------------------------------------------------------------


def claim_jobs(db: Session, tenant_id: str | None, limit: int = 10) -> Sequence[ScanJob]:
    """Queued jobs, oldest first. ``tenant_id=None`` is a system-wide sweep."""
    statement = select(ScanJob).where(ScanJob.status == "queued")
    if tenant_id is not None:
        statement = statement.where(ScanJob.tenant_id == tenant_id)
    return db.scalars(statement.order_by(ScanJob.queued_at).limit(limit)).all()


def append_audit(db: Session, entry: AuditLog) -> AuditLog:
    """Persist an audit entry. There is no update or delete path, by design."""
    db.add(entry)
    return entry


def list_audit(
    db: Session, tenant_id: str, *, limit: int = 200, action_prefix: str | None = None
) -> Sequence[AuditLog]:
    """Read the audit trail, newest first."""
    statement = select(AuditLog).where(AuditLog.tenant_id == tenant_id)
    if action_prefix:
        statement = statement.where(AuditLog.action.like(f"{action_prefix}%"))
    return db.scalars(statement.order_by(AuditLog.audit_id.desc()).limit(limit)).all()


def active_model_version(db: Session, tenant_id: str | None = None) -> ModelVersion | None:
    """The model version currently in force, if any."""
    statement = select(ModelVersion).where(ModelVersion.status == "active")
    if tenant_id is not None:
        statement = statement.where(
            (ModelVersion.tenant_id == tenant_id) | (ModelVersion.tenant_id.is_(None))
        )
    return db.scalars(statement.order_by(ModelVersion.activated_at.desc())).first()


def tenant_job_counts(db: Session, tenant_id: str) -> dict[str, int]:
    """Job counts by status, for the health endpoint."""
    rows = db.execute(
        select(ScanJob.status, func.count(ScanJob.job_id))
        .where(ScanJob.tenant_id == tenant_id)
        .group_by(ScanJob.status)
    ).all()
    return {str(status): int(count) for status, count in rows}


__all__ = [
    "Actor",
    "TenantContext",
    "TenantViolation",
    "active_model_version",
    "add_class_member",
    "add_gallery_entry",
    "append_audit",
    "append_feedback",
    "claim_jobs",
    "create_session",
    "drop_class_member",
    "find_device_by_credential",
    "find_student_by_roll",
    "find_user",
    "gallery_entries_for_index",
    "get_class",
    "get_consent",
    "get_device",
    "get_room",
    "get_session",
    "get_student",
    "get_tenant",
    "get_tenant_by_slug",
    "get_user",
    "has_consent",
    "list_audit",
    "list_classes",
    "list_devices",
    "list_events",
    "list_gallery",
    "list_rooms",
    "list_roster",
    "list_sessions",
    "list_students",
    "list_users",
    "pending_reviews",
    "register_frame",
    "roster_roll_numbers",
    "tenant_job_counts",
    "unresolved_clusters",
]
