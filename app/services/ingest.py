"""Frame ingestion: the production path from bytes to attendance records.

WHY THIS MODULE EXISTS
----------------------
W2 built a real perception pipeline (``app.pipeline.perception``): tiled
detection, five-point alignment, measured quality gating. W3 built a real
identity engine (``app.services.identity``): open-set decisions, margins,
rosters, gallery-depth rules. W4 built the tenant schema, consent records and
an append-only audit log.

None of them were on the live path. The only thing that actually ran was
``app.services.attendance.process_frame``, which:

  - used PIL instead of the tiled pipeline, so a face at the frame edge was
    simply never detected;
  - applied no quality gate, so a blurred 12 px face was embedded and matched;
  - called ``gallery_index.search(...).best``, which silently drops the
    runner-up, so a coin flip between two students looked like a confident win;
  - checked neither tenant isolation nor consent.

Each of those is a correctness bug, and two are privacy bugs. The components
existed and were well tested; they were simply not connected. This module is
the wiring.

THE CONTRACT
------------
:func:`ingest_frame` is idempotent on ``frame_id``. The edge retries with
at-least-once semantics, so the same frame will arrive twice, and a duplicate
that creates a second attendance record is a data-integrity bug a teacher
would see as a student marked present twice.

The order of the checks is deliberate and load-bearing: tenant, then session
state, then idempotency, then perception, then identity. Cheap and
security-relevant first.
"""

from __future__ import annotations

import hashlib
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

import numpy as np
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.domain.decision import Decision
from app.core.domain.types import FrameContext
from app.models.tenancy import (
    AttendanceEvent,
    ClassSession,
    Frame,
    ReviewQueueItem,
)
from app.services import tenancy

log = logging.getLogger(__name__)


class IngestRefused(Exception):
    """A frame was refused, with a machine-readable reason.

    Refusals are values, not accidents. A camera pointed at a corridor must be
    refused and logged, not processed quietly and discarded further down where
    nobody can see why.
    """

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass
class IngestOutcome:
    """What happened to one frame. Every field is a fact, not an estimate."""

    frame_id: str
    session_id: int
    #: True when this exact frame_id had already been ingested.
    duplicate: bool = False
    faces_seen: int = 0
    faces_accepted: int = 0
    faces_rejected: int = 0
    events_created: int = 0
    review_items_created: int = 0
    #: Roll numbers marked present by this frame.
    marked_present: list[str] = field(default_factory=list)
    timings_ms: dict[str, float] = field(default_factory=dict)
    #: Non-fatal problems, each a reason string. Never silently dropped.
    notes: list[str] = field(default_factory=list)

    @property
    def accounted_for(self) -> bool:
        """True when every detected face is either accepted or explained.

        A frame with rejected faces is not a failure: a blurred back-row
        student SHOULD be rejected. But a face that vanishes with no reason
        string is a bug, and this property is what a test asserts.
        """
        return self.faces_accepted + self.faces_rejected == self.faces_seen


def content_sha256(content: bytes) -> str:
    """SHA-256 of the frame bytes. The cloud deduplicates on this value."""
    return hashlib.sha256(content).hexdigest()


def pack_embedding(embedding: Any) -> bytes:
    """Serialise a float32 embedding for LargeBinary storage.

    float32, little-endian and C-contiguous, so the bytes can be read back with
    ``np.frombuffer`` without knowing the dimension in advance.
    """
    return np.ascontiguousarray(np.asarray(embedding, dtype=np.float32)).tobytes()


def unpack_embedding(blob: bytes) -> np.ndarray:
    """Inverse of :func:`pack_embedding`."""
    return np.frombuffer(blob, dtype=np.float32)


def _as_utc(value: Any) -> datetime | None:
    """Normalise a device timestamp to timezone-aware UTC, or None.

    Edge devices send ISO-8601 strings, epoch seconds or datetimes, and some
    send naive local times. A naive value is read as UTC rather than as local
    time: guessing local would place every frame in the wrong hour, and the
    error would be invisible until someone compared a register to a CCTV
    timeline.
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=UTC) if value.tzinfo is None else value.astimezone(UTC)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=UTC)
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            return None
        return parsed.replace(tzinfo=UTC) if parsed.tzinfo is None else parsed.astimezone(UTC)
    return None


def new_frame_id() -> str:
    """A client-side frame id.

    UUIDv7-shaped: time-ordered, so a database index on it does not fragment
    on every insert, and collision-free across devices with no coordination.
    """
    return uuid.uuid4().hex


def _roster_with_consent(db: Session, tenant_id: str, class_id: str) -> frozenset[str]:
    """Roll numbers expected in a session, minus everyone without consent.

    A student who has withdrawn consent is removed from the roster, so the
    identity engine treats them as a stranger rather than as a known classmate.
    They are not marked present, and no embedding is stored against their
    record. Their face still counts as UNKNOWN, so the operator can see that
    somebody was in the room without learning who.
    """
    roll_numbers = tenancy.roster_roll_numbers(db, tenant_id, class_id)
    students = tenancy.list_roster(db, tenant_id, class_id)
    with_consent = {
        student.roll_no
        for student in students
        if tenancy.has_consent(db, tenant_id, student.student_id)
    }
    permitted = roll_numbers & with_consent

    withheld = roll_numbers - with_consent
    if withheld:
        # Logged, not raised: one student's withdrawn consent must not stop
        # the other forty from being marked present. But it is never silent,
        # because "why is this one student never present" is a support ticket
        # that needs an answer.
        log.info(
            "students excluded from the session roster for want of consent",
            extra={
                "stage": "consent_exclusion",
                "class_id": class_id,
                "withheld_count": len(withheld),
                "roll_nos": sorted(withheld)[:20],
            },
        )
    return frozenset(permitted)


def _queue_for_review(
    db: Session,
    assessment: Any,
    *,
    tenant_id: str,
    session_id: int,
) -> bool:
    """Queue an unresolved face for a human, once per cluster.

    One row per cluster, not per frame: a student captured in sixteen frames
    must produce one prompt, not sixteen.

    Returns:
        True if a new review item was created.
    """
    cluster_id = assessment.cluster_id or f"evt:{assessment.frame_id}:{assessment.bbox}"
    existing = db.execute(
        select(ReviewQueueItem).where(
            ReviewQueueItem.tenant_id == tenant_id,
            ReviewQueueItem.cluster_id == cluster_id,
        )
    ).scalar_one_or_none()
    if existing is not None:
        return False
    db.add(
        ReviewQueueItem(
            tenant_id=tenant_id,
            session_id=session_id,
            cluster_id=cluster_id,
            proposed_roll_no=assessment.roll_no,
            best_score=assessment.score,
        )
    )
    return True


def ingest_frame(
    db: Session,
    *,
    frame_id: str,
    session_id: int,
    tenant_id: str,
    content: bytes,
    device_id: str | None = None,
    camera_angle_deg: float | None = None,
    zoom: float | None = None,
    device_timestamp: Any = None,
    correlation_id: str | None = None,
) -> IngestOutcome:
    """Ingest one classroom frame. Idempotent on ``frame_id``.

    Args:
        db: Session bound to the tenant's connection.
        frame_id: Client-generated idempotency key from the edge device.
        session_id: The open class session this frame belongs to.
        tenant_id: Owning tenant, from the authenticated device or user. Never
            from the request body.
        content: Encoded image bytes.
        device_id, camera_angle_deg, zoom: Edge provenance.
        device_timestamp: The DEVICE clock. Used for lateness and never
            replaced by the server clock, because a server timestamp would
            silently move every late arrival into the present.
        correlation_id: Ties the frame to the edge-side log.

    Returns:
        An :class:`IngestOutcome` describing exactly what happened.

    Raises:
        IngestRefused: tenant mismatch, unknown session, or a closed session.
        ImageDecodeError: the bytes are not a decodable, safe image.
    """
    started = time.perf_counter()
    outcome = IngestOutcome(frame_id=frame_id, session_id=session_id)

    # --- 1. Session and tenant -----------------------------------------
    session = db.get(ClassSession, session_id)
    if session is None:
        raise IngestRefused("session_not_found", f"session {session_id} does not exist")
    if session.tenant_id != tenant_id:
        raise IngestRefused(
            "tenant_mismatch",
            f"session {session_id} belongs to tenant {session.tenant_id}, not {tenant_id}",
        )
    if session.end_time is not None:
        raise IngestRefused(
            "session_closed",
            f"session {session_id} closed at {session.end_time.isoformat()}",
        )

    # --- 2. Idempotency -------------------------------------------------
    # Before any expensive work. A redelivered frame is a no-op, which is what
    # makes the edge's at-least-once retry safe.
    existing = db.get(Frame, frame_id)
    if existing is not None:
        if existing.tenant_id != tenant_id or existing.session_id != session_id:
            # Same frame_id from a different tenant or session is not a
            # duplicate, it is an attack or a bug. Refused, not ignored.
            raise IngestRefused(
                "frame_id_collision",
                f"frame {frame_id} already exists for tenant {existing.tenant_id} "
                f"session {existing.session_id}",
            )
        digest = content_sha256(content)
        if existing.sha256 is not None and existing.sha256 != digest:
            # Same id, different bytes. A real retry carries identical bytes, so
            # this is a device bug or a reused id. Silently accepting it would
            # mean the stored frame is not the frame the teacher saw, and the
            # register would be confidently wrong.
            raise IngestRefused(
                "frame_id_content_mismatch",
                f"frame {frame_id} was ingested with different content "
                f"(stored {existing.sha256[:12]}, received {digest[:12]})",
            )
        outcome.duplicate = True
        log.info(
            "duplicate frame ignored",
            extra={"stage": "dedup", "frame_id": frame_id, "session_id": session_id},
        )
        return outcome

    # --- 3. Persist the frame ------------------------------------------
    # Before perception, so a crash mid-inference leaves an auditable record
    # that a frame arrived and was not yet processed, rather than nothing.
    #
    # The device clock wins when present, because a server timestamp would
    # silently move every late or slow frame into the present and quietly
    # falsify the lateness monitoring that the calibration work depends on.
    # Naive values are read as UTC; see docs/decisions/0009-utc-timestamps.md.
    captured_at = _as_utc(device_timestamp) or datetime.now(UTC)

    frame = Frame(
        frame_id=frame_id,
        tenant_id=tenant_id,
        session_id=session_id,
        device_id=device_id,
        captured_at=captured_at,
        device_timestamp=device_timestamp,
        camera_angle_deg=camera_angle_deg,
        zoom=zoom,
        correlation_id=correlation_id,
        sha256=content_sha256(content),
    )
    db.add(frame)
    try:
        db.flush()
    except IntegrityError:
        # Concurrent delivery of the same frame_id. The unique constraint is
        # the real guard; the pre-check above is only an optimisation.
        db.rollback()
        outcome.duplicate = True
        return outcome

    # --- 4. Perception: the W2 pipeline, finally on the live path --------
    context = FrameContext(
        frame_id=frame_id,
        session_id=session_id,
        tenant_id=tenant_id,
        captured_at=captured_at,
        camera_angle_deg=camera_angle_deg,
        zoom=zoom,
        correlation_id=correlation_id or "",
    )
    from app.pipeline.perception import process_frame_bytes

    result = process_frame_bytes(content, context)
    outcome.timings_ms.update(result.timings_ms)
    outcome.faces_accepted = len(result.faces)
    outcome.faces_rejected = len(result.rejected)
    outcome.faces_seen = outcome.faces_accepted + outcome.faces_rejected
    outcome.notes.extend(reason for _, reason in result.rejected)

    # --- 5. Identity: the W3 engine, bound to the consent-filtered roster
    roster = _roster_with_consent(db, tenant_id, session.class_id)
    from app.services.identity import build_identity_engine
    from app.services.tenant_index import tenant_indexes

    # The index is this tenant's, not the process-wide legacy one. A global
    # index would let two schools that both number a student "E001" match each
    # other, and would find nothing at all for a tenant whose gallery was
    # enrolled through the v1 API.
    engine = build_identity_engine(tenant_indexes.get(db, tenant_id)).with_roster(roster)

    marked: list[str] = []
    for face in result.faces:
        if face.embedding is None:
            # Accepted by the quality gate but not embedded. Counted, and
            # explained, rather than quietly dropped.
            outcome.notes.append("accepted_without_embedding")
            continue

        bbox = face.observation.bbox
        assessment = engine.assess(
            face.embedding,
            frame_id=frame_id,
            bbox=bbox,
            quality=face.quality,
            crop_bytes=face.aligned_crop,
            camera_angle_deg=camera_angle_deg,
        )

        db.add(
            AttendanceEvent(
                tenant_id=tenant_id,
                session_id=session_id,
                frame_id=frame_id,
                roll_no=assessment.roll_no,
                face_crop_key=None,
                full_frame_key=frame_id,
                embedding=pack_embedding(face.embedding),
                bbox_x=bbox[0],
                bbox_y=bbox[1],
                bbox_w=bbox[2] - bbox[0],
                bbox_h=bbox[3] - bbox[1],
                confidence_score=assessment.score,
                margin_score=assessment.margin,
                detector_score=face.observation.detector_score,
                quality_score=getattr(face.quality, "score", None),
                match_type=assessment.decision.value,
                decision_reason=assessment.reason,
                camera_angle_deg=camera_angle_deg,
                cluster_id=assessment.cluster_id,
                model_version=model_version(),
                captured_at=captured_at,
            )
        )
        db.flush()
        outcome.events_created += 1

        # CONFIRMED with a roll number is an unattended attendance decision.
        # Anything else -- UNCERTAIN or UNKNOWN -- needs a human, and the
        # review item is created once per cluster rather than once per frame,
        # so a student seen in sixteen frames produces one prompt.
        if assessment.decision is Decision.CONFIRMED and assessment.roll_no:
            marked.append(assessment.roll_no)
        elif _queue_for_review(
            db, assessment, tenant_id=tenant_id, session_id=session_id
        ):
            outcome.review_items_created += 1

    outcome.marked_present = sorted(set(marked))
    db.commit()

    outcome.timings_ms["ingest_total_ms"] = (time.perf_counter() - started) * 1000.0
    log.info(
        "frame ingested",
        extra={
            "stage": "ingest_summary",
            "frame_id": frame_id,
            "session_id": session_id,
            "faces_seen": outcome.faces_seen,
            "faces_accepted": outcome.faces_accepted,
            "events_created": outcome.events_created,
            "marked_present": len(outcome.marked_present),
            "ms": round(outcome.timings_ms.get("ingest_total_ms", 0.0), 1),
        },
    )
    return outcome


def model_version() -> str:
    """The active model identity, stamped on every event.

    Without this, an attendance record cannot be traced to the model that
    produced it, and a threshold change becomes unexplainable after the fact.
    """
    try:
        from app.registry.loader import load_registry

        registry = load_registry()
        return f"{registry.detector.name}+{registry.embedder.name}"
    except Exception:  # noqa: BLE001 - provenance must never block ingestion
        return "unknown"


__all__ = [
    "IngestOutcome",
    "IngestRefused",
    "content_sha256",
    "ingest_frame",
    "model_version",
    "new_frame_id",
    "pack_embedding",
    "unpack_embedding",
]
