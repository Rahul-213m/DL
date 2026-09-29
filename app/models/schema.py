"""LEGACY (pre-multi-tenant) ORM tables.

**These are the "before" state of the W4 migration, not the current schema.**
The canonical schema is :mod:`app.models.tenancy`, which adds tenants and
``tenant_id`` to every tenant-owned table.

Why they are still here
-----------------------
1. The Alembic revision ``0002_multi_tenancy`` reads and transforms exactly
   these tables. They must exist in code for that migration to be reviewable
   against a known starting point.
2. ``app/api/routes.py`` still serves the pre-tenant endpoints, and the 23
   original behavioural tests still exercise them. W7 removes both.

They therefore live on a **separate declarative base** *and* under ``legacy_``
table names, so that both schemas can coexist in one test database. The
renaming is not cosmetic: the pre-tenant ``students`` is keyed on ``roll_no``
and the multi-tenant one on ``student_id``, so an unrenamed pair would collide
and the tenancy composite foreign keys would point at the wrong shape.

Alembic targets ``app.models.database.Base`` (the tenancy schema) only; these
legacy tables are never created by a migration. They are dropped when the W4
data migration completes.

Adding a table here requires a matching Alembic revision. ``create_all`` is
never used to build a production schema — see docs/00_audit.md §6.5.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, LargeBinary, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.models.database import Base, utcnow


class LegacyBase(DeclarativeBase):
    """Declarative base for the pre-tenant schema.

    Deliberately NOT :class:`app.models.database.Base`, so these table names
    cannot collide with the tenancy schema in a shared test database.
    """


class Student(LegacyBase):
    """A person who may be marked present.

    ``gallery_embedding_count`` is a denormalised cache. It exists so the
    roster UI can show counts without an aggregate query, and it is explicitly
    repairable via ``POST /system/repair``. The authoritative value is
    ``count(*) FROM face_gallery``.
    """

    __tablename__ = "legacy_students"

    roll_no: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    enrolled_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    gallery_embedding_count: Mapped[int] = mapped_column(Integer, default=0)


class FaceGallery(LegacyBase):
    """One 512-d embedding belonging to one student.

    This table is the **source of truth** for the identity gallery. The vector
    index is a rebuildable cache (see :mod:`app.core.interfaces.vector_index`).
    Nothing may be added here without a resolvable ``source_image_path``, and
    nothing is ever silently dropped on index failure.
    """

    __tablename__ = "legacy_face_gallery"

    gallery_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    roll_no: Mapped[str] = mapped_column(ForeignKey("legacy_students.roll_no"), index=True)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    source_image_path: Mapped[str] = mapped_column(Text)
    #: "enrollment" | "manual_label" | "cluster_label" | "migration"
    added_via: Mapped[str] = mapped_column(String(32))
    added_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class ClassSession(LegacyBase):
    """One lesson-slot during which frames are captured and attendance accrues."""

    __tablename__ = "legacy_class_sessions"

    session_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_id: Mapped[str] = mapped_column(String(100), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class AttendanceEvent(LegacyBase):
    """One detected face in one frame, with the decision taken on it.

    This is the evidence record. ``embedding`` is duplicated from
    ``face_gallery`` deliberately: the evidence must remain analysable even
    after a gallery entry is later re-imported or corrected.
    """

    __tablename__ = "legacy_attendance_events"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("legacy_class_sessions.session_id"), index=True)
    roll_no: Mapped[str | None] = mapped_column(
        ForeignKey("legacy_students.roll_no"), nullable=True, index=True
    )
    face_crop_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_frame_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    bbox: Mapped[str] = mapped_column(String(100))
    confidence_score: Mapped[float] = mapped_column(Float)
    match_type: Mapped[str] = mapped_column(String(32))
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class ReviewQueue(LegacyBase):
    """A face awaiting a human decision.

    One row per unresolved face. ``proposed_roll_no`` holds the system's best
    guess for the "is this Priya?" confirmation flow; it is never treated as an
    attendance decision on its own.
    """

    __tablename__ = "legacy_review_queue"

    review_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("legacy_attendance_events.event_id"), unique=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    proposed_roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resolved_roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resolved_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


__all__: list[str] = [
    "Any",
    "AttendanceEvent",
    "Base",
    "ClassSession",
    "FaceGallery",
    "Index",
    "LegacyBase",
    "ReviewQueue",
    "Student",
]
