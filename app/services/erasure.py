"""Removal of one student's biometric material.

Two triggers reach this module and they are not the same thing:

* **Consent withdrawal** -- the student or guardian revokes permission. The
  gallery entry must stop being matchable, because continuing to match a face
  after permission is withdrawn is processing without consent.
* **Erasure** (DPDP Act) -- a data-subject request. Everything biometric goes,
  and the fact that it went is kept.

Both paths need the same two things done in the same order, so they share one
implementation rather than two that drift apart.

The ordering is the whole subtlety. The in-process vector index must be told
which exemplars to drop, and the only record of which exemplars those were is
the database rows -- so the ids and object keys are read *before* the rows are
deleted or nulled. Do the statements in the other order and the response
reports a clean erasure while the student's face is still matchable in memory
until the next process restart.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, cast

from sqlalchemy import delete, select, update
from sqlalchemy.engine import CursorResult

from app.models import tenancy as models

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy.orm import Session


@dataclass(frozen=True)
class BiometricRemoval:
    """What a removal actually changed, for the audit trail and the response.

    ``object_keys`` is reported rather than acted on: no storage bucket is
    configured, so claiming these were deleted would be a lie in an API
    response to a privacy request. The count is the number of objects that
    still hold this student's face after the request.
    """

    gallery_rows_removed: int
    attendance_events_cleared: int
    index_entries_removed: int
    object_keys: list[str] = field(default_factory=list)
    student_deactivated: bool = False

    @property
    def pending_object_deletion(self) -> int:
        return len(self.object_keys)

    def as_audit_details(self) -> dict[str, Any]:
        return {
            "gallery_rows_removed": self.gallery_rows_removed,
            "attendance_events_cleared": self.attendance_events_cleared,
            "index_entries_removed": self.index_entries_removed,
            "object_keys_pending_deletion": self.pending_object_deletion,
        }

    def as_response(self, *, student_id: str, erased_at: datetime | None) -> dict[str, Any]:
        from app.core.domain.timeutil import iso_utc

        return {
            "student_id": student_id,
            "erased_at": iso_utc(erased_at) if erased_at is not None else None,
            "gallery_rows_removed": self.gallery_rows_removed,
            "attendance_events_cleared": self.attendance_events_cleared,
            "index_entries_removed": self.index_entries_removed,
            "pending_object_deletion": self.pending_object_deletion,
            "pending_object_keys": self.object_keys,
            "retained": ["audit trail", "the fact of erasure", "aggregate attendance counts"],
        }


def remove_gallery_entries(db: Session, tenant_id: str, student_id: str) -> BiometricRemoval:
    """Stop a student being matchable, and drop the rows behind them.

    Used by consent withdrawal, where the student stays on the roster and only
    the biometric material goes, and by erasure, which additionally marks the
    student inactive. The caller decides that second part, so a withdrawn
    student can be re-enrolled without re-creating the person.

    Caller must commit. Nothing here commits, because withdrawal wants the
    consent record and the removal in one transaction: a withdrawal that
    succeeded while the gallery survived would be worse than a failed one.
    """
    from app.services.tenant_index import tenant_indexes

    # Read first. After the delete below there is nothing left to ask, and the
    # erased student's vectors would stay in the index until a restart.
    gallery_ids = list(
        db.scalars(
            select(models.FaceGallery.gallery_id).where(
                models.FaceGallery.tenant_id == tenant_id,
                models.FaceGallery.student_id == student_id,
                models.FaceGallery.removed_at.is_(None),
            )
        ).all()
    )
    object_keys = set(
        db.scalars(
            select(models.FaceGallery.source_object_key).where(
                models.FaceGallery.tenant_id == tenant_id,
                models.FaceGallery.student_id == student_id,
                models.FaceGallery.source_object_key.is_not(None),
            )
        ).all()
    )

    index_entries_removed = sum(
        1 for gallery_id in gallery_ids if tenant_indexes.remove(db, tenant_id, gallery_id)
    )

    # Gallery rows are hard deleted rather than soft deleted: a withdrawn
    # student's vector is biometric data, and "we kept it but flagged it" is
    # not a withdrawal.
    gallery_rows_removed = cast(
        "CursorResult[Any]",
        db.execute(
            delete(models.FaceGallery).where(
                models.FaceGallery.tenant_id == tenant_id,
                models.FaceGallery.student_id == student_id,
            )
        ),
    ).rowcount

    return BiometricRemoval(
        gallery_rows_removed=gallery_rows_removed,
        attendance_events_cleared=0,
        index_entries_removed=index_entries_removed,
        object_keys=sorted(key for key in object_keys if key),
    )


def erase_student(db: Session, tenant_id: str, student: models.Student) -> BiometricRemoval:
    """Full DPDP erasure: gallery, historical event vectors, and deactivation.

    The attendance rows are kept, with the vector and the student link removed,
    because an attendance register that erases its own evidence cannot be
    defended in a dispute and is not what was asked for: the ask was to remove
    the biometric template, not to invent a gap in the record.
    """
    from app.services.tenant_index import tenant_indexes

    now = datetime.now(UTC)
    student_id = student.student_id

    gallery_ids = list(
        db.scalars(
            select(models.FaceGallery.gallery_id).where(
                models.FaceGallery.tenant_id == tenant_id,
                models.FaceGallery.student_id == student_id,
            )
        ).all()
    )
    # Scoped to this student, and read before the nulling update below. Reading
    # it afterwards returns nothing, which is how a privacy response ends up
    # claiming zero pending objects while crops sit in the bucket.
    object_keys = set(
        db.scalars(
            select(models.AttendanceEvent.face_crop_key).where(
                models.AttendanceEvent.tenant_id == tenant_id,
                models.AttendanceEvent.student_id == student_id,
                models.AttendanceEvent.face_crop_key.is_not(None),
            )
        ).all()
    ) | set(
        db.scalars(
            select(models.FaceGallery.source_object_key).where(
                models.FaceGallery.tenant_id == tenant_id,
                models.FaceGallery.student_id == student_id,
                models.FaceGallery.source_object_key.is_not(None),
            )
        ).all()
    )

    index_entries_removed = sum(
        1 for gallery_id in gallery_ids if tenant_indexes.remove(db, tenant_id, gallery_id)
    )

    gallery_rows_removed = cast(
        "CursorResult[Any]",
        db.execute(
            delete(models.FaceGallery).where(
                models.FaceGallery.tenant_id == tenant_id,
                models.FaceGallery.student_id == student_id,
            )
        ),
    ).rowcount
    events_cleared = cast(
        "CursorResult[Any]",
        db.execute(
            update(models.AttendanceEvent)
            .where(
                models.AttendanceEvent.tenant_id == tenant_id,
                models.AttendanceEvent.student_id == student_id,
            )
            .values(
                embedding=b"",
                student_id=None,
                face_crop_key=None,
                match_type="erased",
                decision_reason="erased on data-subject request",
            )
        ),
    ).rowcount

    student.erased_at = now
    student.is_active = False
    student.gallery_embedding_count = 0
    db.execute(
        update(models.ClassMember)
        .where(
            models.ClassMember.tenant_id == tenant_id,
            models.ClassMember.student_id == student_id,
        )
        .values(dropped_at=now)
    )

    return BiometricRemoval(
        gallery_rows_removed=gallery_rows_removed,
        attendance_events_cleared=events_cleared,
        index_entries_removed=index_entries_removed,
        object_keys=sorted(key for key in object_keys if key),
        student_deactivated=True,
    )
