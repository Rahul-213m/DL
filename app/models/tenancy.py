"""Multi-tenant ORM schema.

Tenancy model
-------------
**Shared database, shared schema, ``tenant_id`` discriminator on every
tenant-owned table, enforced at the query layer.** See
``docs/decisions/0007-multitenancy.md`` for the alternatives and why this one.

The rules this schema makes possible to enforce:

1. Every tenant-owned table has a non-null ``tenant_id`` with an index.
2. A composite foreign key means a child row can never reference a parent in a
   different tenant. This is a *database* guarantee, not a code convention, so
   a bug in one service cannot leak data across a college boundary.
3. Embeddings are unique per (tenant, roll_no, hash) rather than per roll_no,
   so two colleges can both have a student R1.
4. The audit log is append-only: no UPDATE or DELETE path exists in the
   application, and a database trigger documents the intent at the storage
   layer too.
5. Consent is a first-class record. No consent, no enrollment -- enforced in
   :mod:`app.services.consent` and tested for it.

Migration strategy
------------------
Every legacy table predates tenancy. Adding a non-null ``tenant_id`` to a
populated table requires a three-step expand/migrate/contract migration, which
is **W4's second Alembic revision** and is deliberately separate from this
module so it can be reviewed on its own.
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    LargeBinary,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base, utcnow

log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

ROLE_ADMIN = "admin"
ROLE_TEACHER = "teacher"
ROLE_READONLY = "readonly"
ROLES = (ROLE_ADMIN, ROLE_TEACHER, ROLE_READONLY)

CONSENT_GRANTED = "granted"
CONSENT_WITHDRAWN = "withdrawn"
CONSENT_PENDING = "pending"
CONSENT_STATES = (CONSENT_GRANTED, CONSENT_WITHDRAWN, CONSENT_PENDING)

DEVICE_PENDING = "pending"
DEVICE_ACTIVE = "active"
DEVICE_REVOKED = "revoked"
DEVICE_STATES = (DEVICE_PENDING, DEVICE_ACTIVE, DEVICE_REVOKED)

#: What an edge node may do unless an operator grants more. Upload-only, so a
#: stolen camera credential cannot read the roster or export a register.
DEFAULT_DEVICE_SCOPES = '["frames:upload"]'
#: The full set of scopes a device may ever hold. Deliberately small: a device
#: is not a person, and "device can also do X" is a design question, not a
#: deployment detail.
KNOWN_DEVICE_SCOPES = frozenset({"frames:upload", "frames:upload:high", "heartbeat:write"})

MODEL_PENDING = "pending"
MODEL_ACTIVE = "active"
MODEL_REJECTED = "rejected"
MODEL_ROLLED_BACK = "rolled_back"
MODEL_STATES = (MODEL_PENDING, MODEL_ACTIVE, MODEL_REJECTED, MODEL_ROLLED_BACK)

JOB_QUEUED = "queued"
JOB_RUNNING = "running"
JOB_SUCCEEDED = "succeeded"
JOB_FAILED = "failed"
JOB_DEAD = "dead"
JOB_STATES = (JOB_QUEUED, JOB_RUNNING, JOB_SUCCEEDED, JOB_FAILED, JOB_DEAD)

FEEDBACK_ASSIGN_EXISTING = "assign_existing"
FEEDBACK_CREATE_NEW = "create_new"
FEEDBACK_VISITOR = "visitor"
FEEDBACK_SKIP = "skip"
FEEDBACK_CONFIRM = "confirm"
FEEDBACK_REJECT = "reject"
FEEDBACK_ACTIONS = (
    FEEDBACK_ASSIGN_EXISTING,
    FEEDBACK_CREATE_NEW,
    FEEDBACK_VISITOR,
    FEEDBACK_SKIP,
    FEEDBACK_CONFIRM,
    FEEDBACK_REJECT,
)


def _new_id() -> str:
    """UUIDv4 hex for surrogate keys.

    UUIDs rather than auto-increment integers: tenant data will be exported
    and imported between environments, and a sequential integer leaks volume
    information and collides on merge.
    """
    return uuid.uuid4().hex


class Tenant(Base):
    """A college, or any billable organisation.

    ``slug`` is stable and used in URLs and in device provisioning. It is
    immutable once created, because edge devices are provisioned against it.
    """

    __tablename__ = "tenants"

    tenant_id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_new_id)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    region: Mapped[str] = mapped_column(String(64), default="ap-south-1")
    #: Per-tenant encryption context. Null in dev; required in production.
    kms_key_arn: Mapped[str | None] = mapped_column(String(512), nullable=True)
    #: Retention policy overrides, if the college's rules differ from ours.
    retention_override_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (CheckConstraint("length(slug) >= 2", name="ck_tenant_slug_len"),)

    def __repr__(self) -> str:
        return f"<Tenant {self.slug}>"


class User(Base):
    """A human who can log in. Always belongs to exactly one tenant.

    ``password_hash`` is a bcrypt digest produced by
    :mod:`app.core.security`. The plaintext never leaves the request.
    """

    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_new_id)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.tenant_id"), index=True)
    email: Mapped[str] = mapped_column(String(320))
    display_name: Mapped[str] = mapped_column(String(200))
    password_hash: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(20), default=ROLE_READONLY)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    #: Sessions invalidated before this instant (logout-all, password change).
    tokens_valid_after: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        # Email is unique WITHIN a tenant: the same person may be an admin at
        # one college and a read-only viewer at another.
        UniqueConstraint("tenant_id", "email", name="uq_user_tenant_email"),
        CheckConstraint(f"role in {ROLES}", name="ck_user_role"),
        Index("ix_user_tenant_role", "tenant_id", "role"),
    )


class Device(Base):
    """An edge node: the classroom computer running the ROS stack.

    Devices authenticate with their own credential, never with a human's. The
    scope is upload-only: a stolen device credential must not be able to read
    attendance records, change a roster, or impersonate a teacher.
    """

    __tablename__ = "devices"

    device_id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_new_id)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.tenant_id"), index=True)
    #: Human-readable label, e.g. "CS101-room-4".
    name: Mapped[str] = mapped_column(String(120))
    room_id: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    #: SHA-256 of the device secret. The plaintext is shown once, at
    #: provisioning, and is never stored or logged.
    credential_hash: Mapped[str] = mapped_column(String(128))
    #: JSON array of granted scopes, e.g. ``["frames:upload"]``. Stored as text
    #: rather than a join table because the list is tiny, read on every single
    #: authenticated frame, and never queried by value across devices. A
    #: device is upload-only by default; granting anything else is an explicit
    #: act so that a compromised camera cannot read the roster.
    scopes: Mapped[str] = mapped_column(Text, default=DEFAULT_DEVICE_SCOPES)
    status: Mapped[str] = mapped_column(String(20), default=DEVICE_PENDING)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    #: Agent version, so a fleet can be audited after an update.
    agent_version: Mapped[str | None] = mapped_column(String(32), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_device_tenant_name"),
        CheckConstraint(f"status in {DEVICE_STATES}", name="ck_device_status"),
    )

    def scopes_list(self) -> list[str]:
        """The granted scopes, or upload-only if the column is corrupt.

        A malformed value must not become an empty set that silently denies
        every frame, nor an error that locks the classroom out mid-lesson, so
        the fallback is the safe default and the parse failure is logged.
        """
        try:
            parsed: object = json.loads(self.scopes or DEFAULT_DEVICE_SCOPES)
        except (TypeError, ValueError):
            log.warning(
                "device scopes unparseable; defaulting to upload-only",
                extra={"stage": "auth", "device_id": self.device_id},
            )
            return json.loads(DEFAULT_DEVICE_SCOPES)  # type: ignore[no-any-return]
        if not isinstance(parsed, list) or not all(isinstance(s, str) for s in parsed):
            log.warning(
                "device scopes malformed; defaulting to upload-only",
                extra={"stage": "auth", "device_id": self.device_id},
            )
            return json.loads(DEFAULT_DEVICE_SCOPES)  # type: ignore[no-any-return]
        return parsed


class Room(Base):
    """A physical classroom, with the geometry the scan planner needs."""

    __tablename__ = "rooms"

    room_id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_new_id)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.tenant_id"), index=True)
    code: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(200))
    #: Geometry in metres. Drives the pixels-per-face calculation in
    #: docs/hardware/pixels_per_face.md. UNVERIFIED until measured on site.
    width_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    depth_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    camera_height_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    seat_count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    #: Serialised servo calibration, e.g. {"pan_min": -90, "pan_max": 90}.
    calibration_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_room_tenant_code"),
        UniqueConstraint("tenant_id", "room_id", name="uq_room_tenant_room"),
    )


class Class(Base):
    """A course section taught in a room."""

    __tablename__ = "classes"

    class_id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_new_id)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.tenant_id"), index=True)
    room_id: Mapped[str] = mapped_column(String(32), nullable=True)
    code: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(200))
    #: Who may mark attendance for this class. Empty means any teacher.
    teacher_user_ids: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_class_tenant_code"),
        # Required as a composite-FK target by class_members.
        UniqueConstraint("tenant_id", "class_id", name="uq_class_tenant_class"),
    )


class Student(Base):
    """A person enrolled in the college.

    Consent is NOT optional: a student without a ``granted`` consent record is
    refused enrollment by :mod:`app.services.consent`. That is the DPDP Act
    2023 / GDPR requirement made structural rather than procedural.
    """

    __tablename__ = "students"

    student_id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_new_id)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.tenant_id"), index=True)
    roll_no: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    #: Denormalised cache of count(*) from face_gallery. Repairable.
    gallery_embedding_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    #: Set when an erasure request is being honoured; see docs/compliance.md.
    erased_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("tenant_id", "roll_no", name="uq_student_tenant_roll"),
        # Required as a composite-FK target by class_members and face_gallery.
        UniqueConstraint("tenant_id", "student_id", name="uq_student_tenant_student"),
        Index("ix_student_tenant_name", "tenant_id", "name"),
    )


class ClassMember(Base):
    """Roster membership.

    This table is what makes the per-class roster possible. Without it,
    ``absentees()`` compares against every enrolled student, which was the
    legacy behaviour and is wrong the moment a college has more than one class
    (docs/00_audit.md 4.6).
    """

    __tablename__ = "class_members"

    tenant_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    class_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    dropped_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    #: Optional seat identifier, e.g. "row-3-seat-7". Enables seat-map priors.
    seat_label: Mapped[str | None] = mapped_column(String(32), nullable=True)

    __table_args__ = (
        # No unique constraint on (tenant_id, class_id) here, and the comment
        # that used to claim otherwise was wrong: a composite FK needs its
        # target columns unique on the *referenced* table, and ``classes``
        # already declares that pair unique. Declaring it here as well capped
        # every class at exactly one student. Membership uniqueness is the
        # composite primary key above.
        # Composite FKs: a class member can never link a student from another
        # tenant, because the referenced rows themselves carry tenant_id.
        ForeignKeyConstraint(
            ["tenant_id", "class_id"],
            ["classes.tenant_id", "classes.class_id"],
            name="fk_class_member_class",
        ),
        ForeignKeyConstraint(
            ["tenant_id", "student_id"],
            ["students.tenant_id", "students.student_id"],
            name="fk_class_member_student",
        ),
        Index("ix_class_member_class_active", "class_id", "dropped_at"),
        # Every query filters on tenant_id first; without a leading index
        # PostgreSQL cannot use ix_class_member_class_active for it.
        Index("ix_class_member_tenant_class", "tenant_id", "class_id", "dropped_at"),
    )


class TimetableSlot(Base):
    """When a class is expected to run. Drives autonomous scanning (W8)."""

    __tablename__ = "timetable_slots"

    slot_id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_new_id)
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.tenant_id"), index=True)
    class_id: Mapped[str] = mapped_column(String(32), index=True)
    day_of_week: Mapped[int] = mapped_column(Integer)  # 0=Monday
    start_time: Mapped[str] = mapped_column(String(5))  # "09:00" local
    end_time: Mapped[str] = mapped_column(String(5))
    #: Scans to run per slot: a mid-lesson rescan catches late arrivals.
    scan_count: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (
        CheckConstraint("day_of_week between 0 and 6", name="ck_slot_day"),
        CheckConstraint("scan_count >= 1", name="ck_slot_scans"),
    )


class ClassSession(Base):
    """One lesson-slot during which frames are captured and attendance accrues.

    Renamed from the legacy ``class_sessions`` in the W4 migration; the
    semantics are extended, not changed. Nine of the eleven legacy rows had a
    NULL ``end_time`` (docs/00_audit.md 4.9), so close-out is now mandatory.
    """

    __tablename__ = "class_sessions"

    session_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(32), index=True)
    class_id: Mapped[str] = mapped_column(String(32), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    close_reason: Mapped[str | None] = mapped_column(String(20), nullable=True)
    #: True when the session closed before the scan plan finished.
    is_incomplete: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    #: UNVERIFIED count, denormalised for the operator's opening summary.
    present_count: Mapped[int] = mapped_column(Integer, default=0)
    absent_count: Mapped[int] = mapped_column(Integer, default=0)
    unverified_count: Mapped[int] = mapped_column(Integer, default=0)

    __table_args__ = (
        CheckConstraint("end_time IS NULL OR end_time >= start_time", name="ck_session_window"),
        Index("ix_session_tenant_class", "tenant_id", "class_id", "start_time"),
    )


class Frame(Base):
    """One captured classroom frame.

    ``frame_id`` is client-generated (UUIDv7) by the edge device and is the
    idempotency key for the whole pipeline. A redelivered frame is a no-op at
    every downstream stage, which is what makes at-least-once delivery safe
    (see docs/decisions/0003-edge-cloud-protocol.md).
    """

    __tablename__ = "frames"

    frame_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(32), index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("class_sessions.session_id"), index=True)
    device_id: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, index=True)
    #: The DEVICE clock, not the receipt time. Lateness depends on it and a
    #: server-side timestamp would silently move every late arrival.
    device_timestamp: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    camera_angle_deg: Mapped[float | None] = mapped_column(Float, nullable=True)
    zoom: Mapped[float | None] = mapped_column(Float, nullable=True)
    width_px: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height_px: Mapped[int | None] = mapped_column(Integer, nullable=True)
    object_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    __table_args__ = (Index("ix_frame_tenant_session", "tenant_id", "session_id", "captured_at"),)


class FaceGallery(Base):
    """One embedding belonging to one student.

    Uniqueness is per (tenant, roll_no, embedding hash). The hash lets a
    retried enrollment be a no-op instead of a duplicate vector, which matters
    because a re-delivered frame would otherwise inflate a gallery and skew
    the nearest-neighbour statistics.
    """

    __tablename__ = "face_gallery"

    gallery_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(32), index=True)
    student_id: Mapped[str] = mapped_column(String(32), index=True)
    roll_no: Mapped[str] = mapped_column(String(64), index=True)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    #: Hash of the normalised embedding, for deduplication.
    embedding_hash: Mapped[str] = mapped_column(String(64))
    source_object_key: Mapped[str] = mapped_column(Text)
    #: "enrollment" | "manual_label" | "cluster_label" | "migration"
    added_via: Mapped[str] = mapped_column(String(32))
    #: Which model produced this vector. A model change must be able to find
    #: exactly the rows that need re-embedding.
    model_version: Mapped[str] = mapped_column(String(64), default="unknown")
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    added_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    removed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("tenant_id", "roll_no", "embedding_hash", name="uq_gallery_dedup"),
        ForeignKeyConstraint(
            ["tenant_id", "student_id"],
            ["students.tenant_id", "students.student_id"],
            name="fk_gallery_student",
        ),
        Index("ix_gallery_tenant_model", "tenant_id", "model_version", "removed_at"),
    )


class AttendanceEvent(Base):
    """One detected face in one frame, with the decision taken on it.

    The evidence record. ``embedding`` is duplicated from ``face_gallery`` on
    purpose: the evidence must stay analysable after the gallery entry is
    re-imported or the student is re-enrolled.
    """

    __tablename__ = "attendance_events"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(32), index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("class_sessions.session_id"), index=True)
    frame_id: Mapped[str] = mapped_column(String(64), index=True)
    student_id: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    face_crop_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_frame_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    bbox_x: Mapped[int] = mapped_column(Integer, default=0)
    bbox_y: Mapped[int] = mapped_column(Integer, default=0)
    bbox_w: Mapped[int] = mapped_column(Integer, default=0)
    bbox_h: Mapped[int] = mapped_column(Integer, default=0)
    confidence_score: Mapped[float] = mapped_column(Float)
    #: Gap to the runner-up. Stored because it is what distinguishes a clear
    #: win from a coin flip, and the audit showed the legacy code could not.
    margin_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    detector_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    #: "auto" | "low_conf_confirm" | "review" | "manual_label" | "dismissed"
    match_type: Mapped[str] = mapped_column(String(32))
    #: Machine-readable decision cause, for threshold calibration.
    decision_reason: Mapped[str | None] = mapped_column(String(48), nullable=True)
    camera_angle_deg: Mapped[float | None] = mapped_column(Float, nullable=True)
    cluster_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    model_version: Mapped[str] = mapped_column(String(64), default="unknown")
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    __table_args__ = (
        CheckConstraint("bbox_w >= 0 AND bbox_h >= 0", name="ck_event_bbox"),
        Index("ix_event_tenant_session_student", "tenant_id", "session_id", "roll_no"),
    )


class ReviewQueueItem(Base):
    """A face awaiting a human decision.

    One row per unresolved CLUSTER, not per frame, which is the difference
    between a teacher seeing one prompt for a person and seeing eight.
    """

    __tablename__ = "review_queue"

    review_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(32), index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("class_sessions.session_id"), index=True)
    cluster_id: Mapped[str] = mapped_column(String(64), index=True)
    #: "pending" | "resolved" | "dismissed" | "skipped"
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    proposed_roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resolved_roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    #: The AUTHENTICATED user id, never a client-asserted name. The audit
    #: trail is worthless if the actor is whatever the request body said.
    resolved_by_user_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    best_crop_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    best_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    #: How many times this cluster has been shown and skipped. Drives the
    #: rate-limited re-ask policy.
    ask_count: Mapped[int] = mapped_column(Integer, default=0)
    last_asked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        UniqueConstraint("tenant_id", "cluster_id", name="uq_review_tenant_cluster"),
        Index("ix_review_tenant_status", "tenant_id", "status", "ask_count"),
    )


class FeedbackEvent(Base):
    """Every human interaction with the system, permanently.

    Append-only. This is the substrate for the "what did it learn from my
    feedback" summary, for the unknown-rate trend, and for proving who
    changed which attendance record.
    """

    __tablename__ = "feedback_events"

    feedback_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(32), index=True)
    session_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    review_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    cluster_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_id: Mapped[str] = mapped_column(String(32), index=True)
    action: Mapped[str] = mapped_column(String(24))
    roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    #: What the system guessed, so "corrected from X to Y" is measurable.
    previous_guess: Mapped[str | None] = mapped_column(String(64), nullable=True)
    applied: Mapped[bool] = mapped_column(Boolean, default=True)
    #: False when the operator asked to be re-asked later.
    skipped: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    __table_args__ = (
        CheckConstraint(f"action in {FEEDBACK_ACTIONS}", name="ck_feedback_action"),
        Index("ix_feedback_tenant_created", "tenant_id", "created_at"),
    )


class ConsentRecord(Base):
    """A student's consent to biometric processing, and its provenance.

    **No consent, no enrollment.** :mod:`app.services.consent` refuses to add
    a gallery entry for a student without a ``granted`` record, and
    :func:`app.services.erasure` removes one on withdrawal. This is the DPDP
    Act 2023 / GDPR requirement made structural (NEEDS LAWYER to confirm the
    exact wording is sufficient -- see docs/compliance.md).
    """

    __tablename__ = "consent_records"

    consent_id: Mapped[str] = mapped_column(String(32), primary_key=True, default=_new_id)
    tenant_id: Mapped[str] = mapped_column(String(32), index=True)
    student_id: Mapped[str] = mapped_column(String(32), index=True)
    state: Mapped[str] = mapped_column(String(20), default=CONSENT_PENDING)
    #: Free-text record of what was agreed, e.g. the signed form's reference.
    purpose: Mapped[str] = mapped_column(Text)
    granted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    withdrawn_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    #: Retention the student asked for, in days. Null means the tenant default.
    retention_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    #: SHA-256 of the signed consent artefact, for audit without storing the
    #: artefact itself.
    evidence_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    __table_args__ = (
        # Deliberately NOT unique on (tenant_id, student_id). Consent is a
        # ledger, not a slot: withdrawing and re-granting must leave the
        # earlier entries in place, because "this student consented on the
        # 3rd, withdrew on the 9th, consented again on the 12th" is the only
        # record that can answer a regulator's question. The current state is
        # the newest row, resolved by created_at.
        Index("ix_consent_tenant_student_created", "tenant_id", "student_id", "created_at"),
        CheckConstraint(f"state in {CONSENT_STATES}", name="ck_consent_state"),
    )


class ModelVersion(Base):
    """A gallery/embedder version and its measured performance.

    Exists so a model change is a reversible, auditable act rather than a
    hopeful deployment. The regression gate in W7 reads
    ``validation_tar_far`` and refuses to activate a version that scores worse
    than the incumbent.
    """

    __tablename__ = "model_versions"

    model_version: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    detector_key: Mapped[str] = mapped_column(String(64))
    embedder_key: Mapped[str] = mapped_column(String(64))
    #: Licence metadata mirrored from the registry, so the record survives a
    #: code change or a config change.
    license_name: Mapped[str] = mapped_column(String(64))
    commercial_use: Mapped[bool] = mapped_column(Boolean, default=False)
    weights_sha256: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default=MODEL_PENDING)
    #: MEASURED on the frozen validation set. Null until measured; the
    #: regression gate refuses a null.
    validation_tar: Mapped[float | None] = mapped_column(Float, nullable=True)
    validation_far: Mapped[float | None] = mapped_column(Float, nullable=True)
    validation_dataset: Mapped[str | None] = mapped_column(String(200), nullable=True)
    measured_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    activated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    __table_args__ = (CheckConstraint(f"status in {MODEL_STATES}", name="ck_model_status"),)


class ScanJob(Base):
    """A unit of background work, with a status an operator can see.

    Replaces ``BackgroundTasks``, which lost work silently on restart
    (docs/00_audit.md 4.7). A job that failed is a row an operator can
    inspect and retry, not a log line nobody reads.
    """

    __tablename__ = "scan_jobs"

    job_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(32), index=True)
    session_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    frame_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    kind: Mapped[str] = mapped_column(String(32))  # "ingest" | "enroll" | "retrain"
    status: Mapped[str] = mapped_column(String(20), default=JOB_QUEUED, index=True)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    queued_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(f"status in {JOB_STATES}", name="ck_job_status"),
        Index("ix_job_tenant_status", "tenant_id", "status", "queued_at"),
    )


class AuditLog(Base):
    """Append-only record of every privileged action.

    There is deliberately no UPDATE or DELETE path in the application. The
    ``append_only`` marker table plus a check constraint document that intent
    at the storage layer as well, so a direct SQL client cannot quietly rewrite
    history either.
    """

    __tablename__ = "audit_log"

    audit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(32), index=True)
    actor_user_id: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    #: "user" | "device" | "system"
    actor_type: Mapped[str] = mapped_column(String(16), default="system")
    #: Dotted action name, e.g. "review.resolve", "student.erase".
    action: Mapped[str] = mapped_column(String(64), index=True)
    resource_type: Mapped[str] = mapped_column(String(32))
    resource_id: Mapped[str] = mapped_column(String(64), nullable=True)
    #: JSON payload. Never contains biometric data, only identifiers.
    detail_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    #: Client IP, for the breach-response trail.
    source_ip: Mapped[str | None] = mapped_column(String(64), nullable=True)
    #: Client clock, not server clock, so a skewed client is visible.
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    #: Correlates every log line, metric and trace for one operation.
    correlation_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)

    __table_args__ = (
        CheckConstraint(f"actor_type in {('user', 'device', 'system')}", name="ck_audit_actor"),
        Index("ix_audit_tenant_occurred", "tenant_id", "occurred_at"),
    )


class UnknownCluster(Base):
    """A person the system could not identify, aggregated across frames.

    This is what makes "one prompt per person" possible. Each new frame that
    matches an existing cluster increments ``sighting_count`` instead of
    creating a new review item.
    """

    __tablename__ = "unknown_clusters"

    cluster_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(32), index=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("class_sessions.session_id"), index=True)
    #: Running mean of member embeddings, for matching a new sighting.
    centroid: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    #: Unit-normalised exemplar, the best-quality member.
    exemplar_embedding: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    exemplar_object_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    bbox_x: Mapped[int] = mapped_column(Integer, default=0)
    bbox_y: Mapped[int] = mapped_column(Integer, default=0)
    bbox_w: Mapped[int] = mapped_column(Integer, default=0)
    bbox_h: Mapped[int] = mapped_column(Integer, default=0)
    camera_angle_deg: Mapped[float | None] = mapped_column(Float, nullable=True)
    sighting_count: Mapped[int] = mapped_column(Integer, default=1)
    #: "unresolved" | "assigned" | "visitor" | "dismissed"
    status: Mapped[str] = mapped_column(String(20), default="unresolved", index=True)
    assigned_roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_seen_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)

    __table_args__ = (Index("ix_cluster_tenant_session", "tenant_id", "session_id", "status"),)


__all__ = [
    "CONSENT_GRANTED",
    "CONSENT_PENDING",
    "CONSENT_STATES",
    "CONSENT_WITHDRAWN",
    "DEVICE_ACTIVE",
    "DEVICE_PENDING",
    "DEVICE_REVOKED",
    "DEVICE_STATES",
    "FEEDBACK_ACTIONS",
    "FEEDBACK_ASSIGN_EXISTING",
    "FEEDBACK_CONFIRM",
    "FEEDBACK_CREATE_NEW",
    "FEEDBACK_REJECT",
    "FEEDBACK_SKIP",
    "FEEDBACK_VISITOR",
    "JOB_DEAD",
    "JOB_FAILED",
    "JOB_QUEUED",
    "JOB_RUNNING",
    "JOB_STATES",
    "JOB_SUCCEEDED",
    "MODEL_ACTIVE",
    "MODEL_PENDING",
    "MODEL_REJECTED",
    "MODEL_ROLLED_BACK",
    "MODEL_STATES",
    "ROLES",
    "ROLE_ADMIN",
    "ROLE_READONLY",
    "ROLE_TEACHER",
    "AttendanceEvent",
    "AuditLog",
    "Class",
    "ClassMember",
    "ClassSession",
    "ConsentRecord",
    "Device",
    "FaceGallery",
    "FeedbackEvent",
    "Frame",
    "ModelVersion",
    "ReviewQueueItem",
    "Room",
    "ScanJob",
    "Student",
    "Tenant",
    "TimetableSlot",
    "UnknownCluster",
    "User",
]
