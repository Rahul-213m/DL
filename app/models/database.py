from datetime import datetime, timezone
from sqlalchemy import DateTime, Float, ForeignKey, Integer, LargeBinary, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.pool import StaticPool
from app.core.config import settings


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"
    roll_no: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    gallery_embedding_count: Mapped[int] = mapped_column(Integer, default=0)


class FaceGallery(Base):
    __tablename__ = "face_gallery"
    gallery_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    roll_no: Mapped[str] = mapped_column(ForeignKey("students.roll_no"), index=True)
    embedding: Mapped[bytes] = mapped_column(LargeBinary)
    source_image_path: Mapped[str] = mapped_column(Text)
    added_via: Mapped[str] = mapped_column(String(32))
    added_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


class ClassSession(Base):
    __tablename__ = "class_sessions"
    session_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_id: Mapped[str] = mapped_column(String(100), index=True)
    start_time: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class AttendanceEvent(Base):
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
    captured_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


class ReviewQueue(Base):
    __tablename__ = "review_queue"
    review_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("attendance_events.event_id"), unique=True)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)
    proposed_roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resolved_roll_no: Mapped[str | None] = mapped_column(String(64), nullable=True)
    resolved_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


engine_options = {"connect_args": {"check_same_thread": False}} if settings.database_url.startswith("sqlite") else {}
if settings.database_url in {"sqlite://", "sqlite:///:memory:"}:
    engine_options["poolclass"] = StaticPool
engine = create_engine(settings.database_url, **engine_options)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db() -> None: Base.metadata.create_all(engine)
