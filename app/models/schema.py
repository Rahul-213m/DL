"""ORM table definitions.

Separate from :mod:`app.models.database` (which owns the engine) so that the
schema can be imported by Alembic autogenerate, by the API layer and by tests
without dragging in connection management.

Adding a table here requires a matching Alembic revision. ``create_all`` is
never used to build a production schema — see docs/00_audit.md §6.5.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, LargeBinary, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base, utcnow


class Student(Base):
    """A person who may be marked present.

    ``gallery_embedding_count`` is a denormalised cache. It exists so the
    roster UI can show counts without an aggregate query, and it is explicitly
    repairable via ``POST /system/repair``. The authoritative value is
    ``count(*) FROM face_gallery``.
    """

    __tablename__ = "students"

    roll_no: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    enrolled_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    gallery_embedding_count: Mapped[int] = mapped_column(Integer, default=0)


class FaceGallery(Base):
    """One 512-d embedding belonging to one student.

    This table is the **source of truth** for the identity gallery. The vector
    index is a rebuildable cache (see :mod:`app.core.interfaces.vector_index`).
    Nothing may be added here without a resolvable ``source_image_path``, and
    nothing is ever silently dropped on index failure.
    """

    __tablename__ = "face_gallery"

    gallery_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    roll_no: Mapped[str] = mapped_column(ForeignKey("students.roll_no"), index=True)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    source_image_path: Mapped[str] = mapped_column(Text)
    #: "enrollment" | "manual_label" | "cluster_label" | "migration"
    added_via: Mapped[str] = mapped_column(String(32))
    added_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class ClassSession(Base):
    """One lesson-slot during which frames are captured and attendance accrues."""

    __tablename__ = "class_sessions"

    session_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_id: Mapped[str] = mapped_column(String(100), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, default=utcnow)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class AttendanceEvent(Base):
    """One detected face in one frame, with the decision taken on it.

    This is the evidence record. ``embedding`` is duplicated from
    ``face_gallery`` deliberately: the evidence must remain analysable even
    after a gallery entry is later re-imported or corrected.
    """

    __tablename__ = "attendance_events"

    event_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("class_sessions.session_id"), index=True)
    roll_no: Mapped[str | None] = mapped_column(ForeignKey("students.roll_no"), nullable=True, index=True)
    face_crop_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_frame_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    bbox: Mapped[str] = mapped_column(String(100))
    confidence_score: Mapped[float] = mapped_column(Float)
    match_type: Mapped[str] = mapped_column(String(32))
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow)


class ReviewQueue(Base):
    """A face awaiting a human decision.

    One row per unresolved face. ``proposed_roll_no`` holds the system's best
    guess for the "is this Priya?" confirmation flow; it is never treated as an
    attendance decision on its own.
    """

    __tablename__ = "review_queue"

    review_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("attendance_events.event_id"), unique=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    proposed_roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resolved_roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resolved_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


__all__: list[str] = [
    "Any",
    "AttendanceEvent",
    "ClassSession",
    "FaceGallery",
    "Index",
    "ReviewQueue",
    "Student",
]
