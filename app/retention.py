"""Retention policy enforcement.

Every stored image has a retention class. The legacy implementation only purged
session frames and face crops, which left ``data/review-context/`` — full
classroom photographs with red boxes drawn on them — on disk forever
(docs/00_audit.md §6.4).

Deleting an image **nulls the path on the evidence row** rather than deleting
the row. The attendance decision and its score remain auditable; only the
biometric image goes. That distinction is what makes "we deleted the photo" and
"we deleted the record" separate, defensible operations.

This module is dry-run by default. Deleting a student's biometric data is
irreversible and must be a deliberate act.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from app.core.config import settings

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RetentionPolicy:
    """One retention class: which paths, how long, and which columns to null."""

    name: str
    days: int
    #: Path prefixes under ``storage_root`` this policy covers.
    subdirectories: tuple[str, ...]
    #: ``(model, column)`` pairs whose value points at a covered image.
    evidence_columns: tuple[tuple[str, str], ...]


def build_policies() -> list[RetentionPolicy]:
    """Construct the policy set from settings."""
    return [
        RetentionPolicy(
            name="raw_frames",
            days=settings.raw_frame_retention_days,
            subdirectories=("sessions",),
            evidence_columns=(("AttendanceEvent", "full_frame_path"),),
        ),
        RetentionPolicy(
            name="face_crops",
            days=settings.face_crop_retention_days,
            subdirectories=("sessions",),
            evidence_columns=(("AttendanceEvent", "face_crop_path"),),
        ),
        RetentionPolicy(
            name="review_context",
            days=settings.review_context_retention_days,
            subdirectories=("review-context",),
            evidence_columns=(),
        ),
        RetentionPolicy(
            name="enrollment_photos",
            days=settings.enrollment_photo_retention_days,
            subdirectories=("enrollment",),
            evidence_columns=(("FaceGallery", "source_image_path"),),
        ),
    ]


def _utc_cutoff(days: int) -> datetime:
    """Return the timestamp before which files are expired."""
    return datetime.now(UTC) - timedelta(days=days)


def _files_older_than(root: Path, subdir: str, cutoff: datetime) -> Iterable[Path]:
    """Yield files under ``root/subdir`` whose mtime predates ``cutoff``."""
    target = root / subdir
    if not target.is_dir():
        return
    for path in target.rglob("*"):
        if not path.is_file():
            continue
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
        except OSError:
            continue
        if mtime < cutoff:
            yield path


def _null_evidence_columns(
    db: Any,
    table: str,
    column: str,
    paths: set[str],
    dry_run: bool,
) -> int:
    """Set ``column`` to NULL for rows pointing at any of ``paths``.

    Returns the number of rows affected (also counted in dry-run mode, so the
    operator sees the blast radius before committing).
    """
    from sqlalchemy import select

    from app.models import schema

    model = getattr(schema, table, None)
    if model is None:
        log.warning("retention: unknown evidence table %s", table)
        return 0
    attr = getattr(model, column)
    affected = 0
    for chunk_start in range(0, len(paths), 500):
        chunk = list(paths)[chunk_start : chunk_start + 500]
        statement = select(model).where(attr.in_(chunk))
        rows = db.execute(statement).scalars().all()
        for row in rows:
            affected += 1
            if not dry_run:
                setattr(row, column, None)
    return affected


def purge_expired(dry_run: bool = True, root: Path | None = None) -> dict[str, Any]:
    """Apply every retention policy.

    Args:
        dry_run: when True (the default) nothing is deleted and no row is
            written; counts are still computed so the operator can review.
        root: override the storage root. Used by tests.

    Returns:
        ``{"deleted": {policy: count}, "nulled_columns": {...}, "errors": [...]}``
    """
    from sqlalchemy.orm import Session

    from app.models.database import SessionLocal

    root = root or settings.storage_root
    deleted: dict[str, int] = {}
    nulled: dict[str, int] = {}
    errors: list[str] = []

    policies = build_policies()
    db: Session | None = None
    if not dry_run:
        db = SessionLocal()

    try:
        for policy in policies:
            cutoff = _utc_cutoff(policy.days)
            expired: set[str] = set()
            for subdir in policy.subdirectories:
                for path in _files_older_than(root, subdir, cutoff):
                    expired.add(str(path))

            deleted[policy.name] = len(expired)
            if not expired:
                continue

            if dry_run:
                log.info(
                    "retention dry-run",
                    extra={"policy": policy.name, "would_delete": len(expired)},
                )
            else:
                for path_string in expired:
                    try:
                        Path(path_string).unlink(missing_ok=True)
                    except OSError as exc:
                        errors.append(f"{policy.name}: could not delete {path_string}: {exc}")

            assert db is not None
            for table, column in policy.evidence_columns:
                count = _null_evidence_columns(db, table, column, expired, dry_run)
                key = f"{table}.{column}"
                nulled[key] = nulled.get(key, 0) + count

        if not dry_run and db is not None:
            db.commit()
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")
        log.exception("retention purge failed", extra={"dry_run": dry_run})
        if db is not None:
            db.rollback()
    finally:
        if db is not None:
            db.close()

    return {"deleted": deleted, "nulled_columns": nulled, "errors": errors, "dry_run": dry_run}


__all__ = ["RetentionPolicy", "build_policies", "purge_expired"]
