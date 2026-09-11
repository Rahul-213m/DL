#!/usr/bin/env python3
"""Purge expired session images while retaining attendance-event audit data."""
from datetime import datetime, timedelta
from pathlib import Path

from app.core.config import settings
from app.models.database import AttendanceEvent, SessionLocal


def purge_old_frames() -> int:
    cutoff = datetime.now().timestamp() - timedelta(days=settings.raw_frame_retention_days).total_seconds()
    root = settings.storage_root / "sessions"
    if not root.exists():
        return 0
    db = SessionLocal()
    removed = 0
    try:
        for category in ("frames", "faces"):
            for path in root.glob(f"**/{category}/*"):
                if not path.is_file() or path.stat().st_mtime >= cutoff:
                    continue
                path_string = str(path)
                path.unlink()
                for event in db.query(AttendanceEvent).filter(AttendanceEvent.face_crop_path == path_string).all():
                    event.face_crop_path = None
                for event in db.query(AttendanceEvent).filter(AttendanceEvent.full_frame_path == path_string).all():
                    event.full_frame_path = None
                removed += 1
        db.commit()
        return removed
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print(f"Purged {purge_old_frames()} expired session image(s).")
