from datetime import datetime, timezone
from pathlib import Path
import io
import logging
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import require_api_key
from app.models.database import AttendanceEvent, ClassSession, FaceGallery, ReviewQueue, SessionLocal, Student
from app.models.schemas import ResolveReview, SessionStart
from app.pipeline.recognizer import recognizer
from app.services.attendance import bbox_context, process_frame
from app.services.gallery import append_gallery, gallery_index, unpack_embedding
from app.storage.local import storage
from PIL import Image
import numpy as np

router = APIRouter(dependencies=[Depends(require_api_key)])
log = logging.getLogger(__name__)
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def normalize_roll_no(raw: str) -> str:
    """Canonicalize a roll number so folder names, form input, and manual labels
    all compare and store identically (trim surrounding whitespace, uppercase)."""
    return (raw or "").strip().upper()

def find_student(db: Session, roll_no: str) -> Student | None:
    """Case- and whitespace-insensitive lookup so an existing row with a legacy
    variant (e.g. 'r3 ' or ' r3') still matches its normalized form."""
    return db.scalar(select(Student).where(func.upper(func.trim(Student.roll_no)) == roll_no))
async def image_bytes(upload: UploadFile) -> bytes:
    if upload.content_type not in {"image/jpeg", "image/png", "image/webp"}: raise HTTPException(415, "Only JPEG, PNG, or WebP images are accepted")
    data = await upload.read()
    if not data or len(data) > settings.max_upload_bytes: raise HTTPException(413, "Invalid or oversized image")
    try:
        with Image.open(io.BytesIO(data)) as image:
            if image.width * image.height > settings.max_image_pixels:
                raise HTTPException(422, f"image exceeds {settings.max_image_pixels:,} pixel safety limit")
            image.verify()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(422, "Upload is not a valid image")
    return data

def extract_enrollment_face(faces: list) -> tuple[bool, any, str]:
    """Extract single or dominant face for enrollment."""
    valid_faces = [
        f for f in faces
        if (f.bbox[2] - f.bbox[0]) >= settings.min_face_size_px
        and (f.bbox[3] - f.bbox[1]) >= settings.min_face_size_px
    ]
    if not valid_faces:
        return False, None, "no face detected above minimum size"
    if len(valid_faces) == 1:
        return True, valid_faces[0], ""
    sorted_faces = sorted(
        valid_faces,
        key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]),
        reverse=True
    )
    largest_area = (sorted_faces[0].bbox[2] - sorted_faces[0].bbox[0]) * (sorted_faces[0].bbox[3] - sorted_faces[0].bbox[1])
    second_area = (sorted_faces[1].bbox[2] - sorted_faces[1].bbox[0]) * (sorted_faces[1].bbox[3] - sorted_faces[1].bbox[1])
    if largest_area >= 2.5 * second_area:
        return True, sorted_faces[0], ""
    return False, None, f"multiple ambiguous faces detected ({len(valid_faces)})"

@router.post("/students/enroll", status_code=status.HTTP_201_CREATED)
async def enroll(roll_no: str = Form(...), name: str = Form(...), images: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    if not 8 <= len(images) <= 15: raise HTTPException(422, "Enrollment requires 8–15 images")
    roll_no = normalize_roll_no(roll_no)
    if not roll_no: raise HTTPException(422, "roll number is required")
    processed=[]
    for index, upload in enumerate(images, 1):
        data = await image_bytes(upload)
        image = np.asarray(Image.open(io.BytesIO(data)).convert("RGB"))
        try: faces = recognizer.detect(image)
        except Exception as exc: log.exception("enrollment inference failed"); raise HTTPException(503, "Face recognition model unavailable") from exc
        ok, face, reason = extract_enrollment_face(faces)
        if not ok: raise HTTPException(422, f"Image {index}: {reason}")
        processed.append((data, face.embedding))
    # Re-enrollment is gallery growth, not a duplicate-student error. This is
    # important once the local photo folder has reached its storage cap: accepted
    # images must still be added to the database gallery.
    student = find_student(db, roll_no)
    if not student:
        student = Student(roll_no=roll_no, name=name)
        db.add(student)
        db.flush()
    for data, embedding in processed:
        path=storage.save(data, f"enrollment/{roll_no}")
        append_gallery(db, roll_no, embedding, path, "enrollment")
        storage.mirror_enrollment_photo(roll_no, data, "upload")
    db.commit()
    return {"roll_no": roll_no, "gallery_embedding_count": student.gallery_embedding_count}

@router.post("/students/import-folders")
def import_enrollment_folders(db: Session = Depends(get_db)):
    """Import one student per folder under ENROLL_PHOTOS_ROOT."""
    root = settings.enrollment_photos_root
    if not root.is_dir():
        raise HTTPException(404, f"Enrollment folder not found: {root}")

    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    imported, skipped = [], []
    seen_this_run: set[str] = set()
    for folder in sorted(path for path in root.iterdir() if path.is_dir()):
        raw_name = folder.name
        roll_no = normalize_roll_no(raw_name)
        image_paths = sorted(path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in allowed_extensions)
        # Normalized roll number already handled earlier in this same run (duplicate
        # folder that only differs by case/whitespace, e.g. 'R3' and 'r3 ').
        if roll_no in seen_this_run:
            skipped.append({"roll_no": raw_name, "reason": "duplicate folder for the same roll number in this import"})
            continue
        seen_this_run.add(roll_no)
        if len(image_paths) < 8:
            skipped.append({"roll_no": roll_no, "reason": "requires at least 8 supported images", "image_count": len(image_paths)})
            continue
        processed = []
        for index, image_path in enumerate(image_paths, 1):
            try:
                data = image_path.read_bytes()
                if not data or len(data) > settings.max_upload_bytes:
                    continue
                Image.open(io.BytesIO(data)).verify()
                image = np.asarray(Image.open(io.BytesIO(data)).convert("RGB"))
                faces = recognizer.detect(image)
                ok, face, _ = extract_enrollment_face(faces)
                if ok:
                    processed.append((data, face.embedding))
            except Exception as exc:
                log.debug("image skipped in folder enrollment", extra={"roll_no": roll_no, "image": image_path.name, "error": str(exc)})
                continue
        if len(processed) < 8:
            skipped.append({
                "roll_no": roll_no,
                "reason": f"only {len(processed)} valid face images extracted (minimum 8 required from {len(image_paths)} files)"
            })
            continue
        try:
            # A folder is an input source, not an immutable first-enrollment
            # record.  Its newly accepted images must grow an existing student's
            # DB gallery too.  The 15-photo policy applies only to the readable
            # ENROLL_PHOTOS mirror below, never to face_gallery.
            student = find_student(db, roll_no)
            created = student is None
            if created:
                student = Student(roll_no=roll_no, name=roll_no)
                db.add(student)
                db.flush()
            for data, embedding in processed:
                path = storage.save(data, f"enrollment/{roll_no}")
                append_gallery(db, roll_no, embedding, path, "enrollment")
                storage.mirror_enrollment_photo(roll_no, data, "import")
            db.commit()
            imported.append({"roll_no": roll_no, "gallery_embedding_count": student.gallery_embedding_count,
                             "added_embedding_count": len(processed),
                             "status": "created" if created else "updated"})
        except IntegrityError:
            # A concurrent request may create the student between our lookup and
            # insert.  Retry as an update so its images are not silently dropped.
            db.rollback()
            student = find_student(db, roll_no)
            if not student:
                log.exception("student was not visible after concurrent insert", extra={"roll_no": roll_no})
                skipped.append({"roll_no": roll_no, "reason": "failed: concurrent enrollment could not be read", "status": "failed"})
                continue
            try:
                for data, embedding in processed:
                    path = storage.save(data, f"enrollment/{roll_no}")
                    append_gallery(db, roll_no, embedding, path, "enrollment")
                    storage.mirror_enrollment_photo(roll_no, data, "import")
                db.commit()
                imported.append({"roll_no": roll_no, "gallery_embedding_count": student.gallery_embedding_count,
                                 "added_embedding_count": len(processed), "status": "updated"})
            except Exception as exc:
                db.rollback()
                log.exception("concurrent folder enrollment update failed", extra={"roll_no": roll_no})
                skipped.append({"roll_no": roll_no, "reason": f"failed: could not update student ({type(exc).__name__})", "status": "failed"})
        except Exception as exc:
            db.rollback()
            log.exception("folder enrollment could not be saved", extra={"roll_no": roll_no})
            skipped.append({"roll_no": roll_no, "reason": f"failed: could not save student ({type(exc).__name__})", "status": "failed"})
    return {"root": str(root), "imported": imported, "skipped": skipped}

@router.post("/session/start", status_code=201)
def start_session(body: SessionStart, db: Session = Depends(get_db)):
    session=ClassSession(class_id=body.class_id); db.add(session); db.commit(); db.refresh(session)
    return {"session_id": session.session_id, "class_id": session.class_id, "start_time": session.start_time}

def _process_background(session_id: int, data: bytes):
    db=SessionLocal()
    try: process_frame(db, session_id, data)
    except Exception: log.exception("frame processing failed", extra={"session_id": session_id}); db.rollback()
    finally: db.close()

@router.post("/session/{session_id}/capture", status_code=202)
async def capture(session_id: int, background_tasks: BackgroundTasks, frame: UploadFile = File(...), db: Session = Depends(get_db)):
    session = db.get(ClassSession, session_id)
    if not session: raise HTTPException(404, "session not found")
    if session.end_time: raise HTTPException(409, "session is closed")
    data = await image_bytes(frame)
    background_tasks.add_task(_process_background, session_id, data)
    return {"message": "frame accepted for asynchronous processing", "session_id": session_id}

@router.get("/session/{session_id}/scores")
def capture_scores(session_id: int, db: Session = Depends(get_db)):
    """Return all attendance events for this session with their scores — used by the threshold playground."""
    if not db.get(ClassSession, session_id): raise HTTPException(404, "session not found")
    events = db.query(AttendanceEvent).filter_by(session_id=session_id).order_by(AttendanceEvent.confidence_score.desc()).all()
    return [{"roll_no": e.roll_no, "score": e.confidence_score, "match_type": e.match_type,
             "face_crop_path": e.face_crop_path, "captured_at": e.captured_at} for e in events]

def _review_queue_items(rows: list[tuple[ReviewQueue, AttendanceEvent]]) -> list[dict]:
    """Serialize pending review records consistently for both queue endpoints."""
    return [
        {
            "review_id": queue.review_id,
            "event_id": event.event_id,
            "session_id": event.session_id,
            "best_guess": queue.proposed_roll_no,
            "face_crop_path": event.face_crop_path,
            "boxed_frame_path": bbox_context(event),
            "confidence_score": event.confidence_score,
            "captured_at": event.captured_at,
        }
        for queue, event in rows
    ]


@router.get("/session/{session_id}/review-queue")
def review_queue(session_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(ReviewQueue, AttendanceEvent)
        .join(AttendanceEvent)
        .filter(AttendanceEvent.session_id == session_id, ReviewQueue.status == "pending")
        .order_by(ReviewQueue.review_id)
        .all()
    )
    return _review_queue_items(rows)


@router.get("/review-queue")
def all_pending_reviews(db: Session = Depends(get_db)):
    """Return every unresolved review, including reviews from older sessions.

    Operators often start a new session before opening the queue. Keeping these
    records visible prevents a low-confidence match from being stranded in the
    session in which it was captured.
    """
    rows = (
        db.query(ReviewQueue, AttendanceEvent)
        .join(AttendanceEvent)
        .filter(ReviewQueue.status == "pending")
        .order_by(AttendanceEvent.session_id.desc(), ReviewQueue.review_id)
        .all()
    )
    return _review_queue_items(rows)

@router.post("/review/{review_id}/resolve")
def resolve(review_id: int, body: ResolveReview, db: Session = Depends(get_db)):
    queue=db.get(ReviewQueue, review_id)
    if not queue: raise HTTPException(404, "review item not found")
    if queue.status != "pending": raise HTTPException(409, "review item is already resolved")
    event=db.get(AttendanceEvent, queue.event_id)
    if not event: raise HTTPException(404, "review item has no attendance event to resolve")
    # A review can be resolved for a roll number with no prior enrollment (new student
    # mid-semester): create the student row so append_gallery's FK is satisfied.
    body.roll_no = normalize_roll_no(body.roll_no)
    if not body.roll_no: raise HTTPException(422, "roll number is required")
    student=find_student(db, body.roll_no)
    if not student:
        student=Student(roll_no=body.roll_no, name=body.name or body.roll_no); db.add(student); db.flush()
    embedding=unpack_embedding(event.embedding)
    try:
        entry=append_gallery(db, body.roll_no, embedding, event.face_crop_path, "manual_label")
    except Exception as exc:
        db.rollback()
        log.exception("review resolution failed to persist gallery entry", extra={"review_id": review_id, "roll_no": body.roll_no})
        raise HTTPException(500, "could not persist the corrected gallery entry") from exc
    # This mirror is best-effort and capped at 15 files. It must never prevent
    # the confirmed label above from reaching the DB gallery.
    try:
        if event.face_crop_path and Path(event.face_crop_path).exists():
            storage.mirror_enrollment_photo(body.roll_no, Path(event.face_crop_path).read_bytes(), "review")
    except Exception:
        log.exception("could not mirror resolved crop into enrollment folder", extra={"review_id": review_id, "roll_no": body.roll_no})
    event.roll_no = body.roll_no
    event.match_type = "manual_label"
    queue.status = "resolved"
    queue.resolved_roll_no = body.roll_no
    queue.resolved_by = body.resolved_by
    queue.resolved_at = datetime.now(timezone.utc)
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        log.exception("review resolution commit failed", extra={"review_id": review_id, "roll_no": body.roll_no})
        raise HTTPException(500, "could not commit the review resolution") from exc
    entry_id, gallery_count = entry.gallery_id, student.gallery_embedding_count
    log.info("review resolved", extra={"review_id": review_id, "roll_no": body.roll_no,
                                       "user": body.resolved_by, "gallery_id": entry_id,
                                       "gallery_embedding_count": gallery_count})
    return {"review_id":review_id,"roll_no":body.roll_no,"status":"resolved",
            "gallery_id":entry_id,"gallery_embedding_count":gallery_count}

@router.post("/system/repair")
def system_repair(db: Session = Depends(get_db)):
    """Repair DB counters/indexes and recreate missing enrollment directories.

    Gallery rows remain authoritative.  When a student's ENROLL_PHOTOS directory
    is absent, copy any still-available gallery source images into the fresh
    directory through the normal capped mirror path.
    """
    fixed = []
    gallery_counts = {roll: n for roll, n in
                      db.query(FaceGallery.roll_no, func.count(FaceGallery.gallery_id)).group_by(FaceGallery.roll_no).all()}
    for student in db.query(Student).all():
        actual = gallery_counts.get(student.roll_no, 0)
        if actual != student.gallery_embedding_count:
            fixed.append({"roll_no": student.roll_no, "was": student.gallery_embedding_count, "now": actual})
            student.gallery_embedding_count = actual
    db.commit()
    recreated_folders: list[str] = []
    mirrored_photos = 0
    for student in db.query(Student).all():
        folder = settings.enrollment_photos_root / student.roll_no
        if folder.is_dir():
            continue
        folder.mkdir(parents=True, exist_ok=True)
        recreated_folders.append(student.roll_no)
        for entry in db.query(FaceGallery).filter_by(roll_no=student.roll_no).order_by(FaceGallery.gallery_id):
            source = Path(entry.source_image_path)
            if not source.is_file():
                continue
            try:
                if storage.mirror_enrollment_photo(student.roll_no, source.read_bytes(), "repair"):
                    mirrored_photos += 1
            except Exception:
                log.exception("could not restore enrollment photo during repair",
                              extra={"roll_no": student.roll_no, "gallery_id": entry.gallery_id})
    gallery_index.rebuild(db)
    return {"repaired": fixed, "repaired_count": len(fixed), "gallery_size": gallery_index.size,
            "recreated_enrollment_folders": recreated_folders,
            "mirrored_enrollment_photos": mirrored_photos}

@router.post("/students/{roll_no}/reimport")
def reimport_student(roll_no: str, db: Session = Depends(get_db)):
    """Re-(re)build one student's gallery from the photos in ENROLL_PHOTOS/<roll_no>/.

    This is the safe remedy for a student whose enrollment never completed (e.g.
    photos exist on disk but the DB has no embeddings), or whose gallery drifted.
    Existing embeddings for the student are cleared first so the result is
    deterministic.
    """
    roll_no = normalize_roll_no(roll_no)
    folder = settings.enrollment_photos_root / roll_no
    if not folder.is_dir():
        raise HTTPException(404, f"no ENROLL_PHOTOS/{roll_no}/ folder to import from")
    allowed = {".jpg", ".jpeg", ".png", ".webp"}
    image_paths = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in allowed)
    if not image_paths:
        raise HTTPException(422, f"ENROLL_PHOTOS/{roll_no}/ contains no supported images")

    processed = []
    rejected = []
    for image_path in image_paths[:15]:
        try:
            data = image_path.read_bytes()
            if not data or len(data) > settings.max_upload_bytes:
                rejected.append(image_path.name); continue
            Image.open(io.BytesIO(data)).verify()
            image = np.asarray(Image.open(io.BytesIO(data)).convert("RGB"))
            ok, face, reason = extract_enrollment_face(recognizer.detect(image))
            if ok:
                processed.append((data, face.embedding))
            else:
                rejected.append(image_path.name)
        except Exception:
            log.exception("reimport: image failed", extra={"roll_no": roll_no, "image": image_path.name})
            rejected.append(image_path.name)

    if len(processed) < 8:
        raise HTTPException(422, f"only {len(processed)} valid face image(s) found (minimum 8 required)")

    student = find_student(db, roll_no)
    if not student:
        student = Student(roll_no=roll_no, name=roll_no); db.add(student); db.flush()
    try:
        db.query(FaceGallery).filter_by(roll_no=student.roll_no).delete()
        student.gallery_embedding_count = 0
        for data, embedding in processed:
            path = storage.save(data, f"enrollment/{student.roll_no}")
            append_gallery(db, student.roll_no, embedding, path, "enrollment")
            storage.mirror_enrollment_photo(student.roll_no, data, "import")
        db.commit()
    except Exception as exc:
        db.rollback()
        log.exception("reimport failed to persist", extra={"roll_no": roll_no})
        raise HTTPException(500, "could not save the rebuilt gallery") from exc
    gallery_index.rebuild(db)
    return {"roll_no": student.roll_no, "gallery_embedding_count": len(processed),
            "rejected_images": rejected}

@router.post("/review/{review_id}/dismiss")
def dismiss_review(review_id: int, db: Session = Depends(get_db)):
    """Dismiss an unidentified/false-positive face without adding it to the student gallery."""
    queue = db.get(ReviewQueue, review_id)
    if not queue:
        raise HTTPException(404, "review item not found")
    if queue.status != "pending":
        raise HTTPException(409, "review item is already resolved or dismissed")
    event = db.get(AttendanceEvent, queue.event_id)
    queue.status = "dismissed"
    queue.resolved_at = datetime.now(timezone.utc)
    if event:
        event.match_type = "dismissed"
    db.commit()
    return {"review_id": review_id, "status": "dismissed"}

@router.post("/review/{review_id}/reopen")
def reopen_review(review_id: int, db: Session = Depends(get_db)):
    """Undo a manual resolution or dismissal and return the face to the pending review queue."""
    queue = db.get(ReviewQueue, review_id)
    if not queue:
        raise HTTPException(404, "review item not found")
    if queue.status not in {"resolved", "dismissed"}:
        raise HTTPException(409, "review item is not resolved or dismissed")

    event = db.get(AttendanceEvent, queue.event_id)
    if queue.status == "resolved":
        resolved_roll_no = queue.resolved_roll_no
        gallery_entry = db.query(FaceGallery).filter_by(
            roll_no=resolved_roll_no,
            source_image_path=event.face_crop_path,
            added_via="manual_label",
        ).order_by(FaceGallery.gallery_id.desc()).first()
        if gallery_entry:
            student = db.get(Student, resolved_roll_no)
            db.delete(gallery_entry)
            if student:
                student.gallery_embedding_count = max(0, student.gallery_embedding_count - 1)

    if event:
        event.roll_no = None
        event.match_type = "review"
    queue.status = "pending"
    queue.resolved_roll_no = None
    queue.resolved_by = None
    queue.resolved_at = None
    db.commit()
    gallery_index.rebuild(db)
    return {"review_id": review_id, "status": "pending"}

# Match types that represent a confirmed attendance decision.
# 'review' / 'low_conf_confirm' / 'dismissed' are unconfirmed drafts and must
# never be reported as present on their own.
CONFIRMED_MATCH_TYPES = ("auto", "manual_label")

@router.get("/session/{session_id}/query/{roll_no}")
def query(session_id: int, roll_no: str, db: Session = Depends(get_db)):
    roll_no = normalize_roll_no(roll_no)
    # Only confirmed labels count as attendance. Among them a human correction
    # (manual_label) must outrank an automatic match, falling back to the
    # highest-confidence confirmed event. Unconfirmed drafts (an auto-guess that
    # was never reviewed, or a bare 'review' row) are surfaced separately as
    # 'pending' so the UI never states presence it cannot stand behind.
    confirmed = (db.query(AttendanceEvent)
                 .filter(AttendanceEvent.session_id == session_id,
                         AttendanceEvent.roll_no == roll_no,
                         AttendanceEvent.match_type.in_(CONFIRMED_MATCH_TYPES))
                 .order_by((AttendanceEvent.match_type != "manual_label"),
                           AttendanceEvent.confidence_score.desc(),
                           AttendanceEvent.event_id.desc())
                 .first())
    if confirmed:
        return {"roll_no": roll_no, "status": "present", "evidence": {
            "face_crop_path": confirmed.face_crop_path,
            "full_frame_path": confirmed.full_frame_path,
            "confidence_score": confirmed.confidence_score,
            "match_type": confirmed.match_type,
            "captured_at": confirmed.captured_at}}
    # Low-confidence candidates intentionally leave AttendanceEvent.roll_no
    # unset until an operator confirms them. Their candidate identity lives in
    # ReviewQueue.proposed_roll_no, so query that field when reporting a
    # pending match; otherwise the Results page incorrectly says "absent".
    pending = (db.query(AttendanceEvent)
               .join(ReviewQueue, ReviewQueue.event_id == AttendanceEvent.event_id)
               .filter(AttendanceEvent.session_id == session_id,
                       ReviewQueue.proposed_roll_no == roll_no,
                       ReviewQueue.status == "pending")
               .first())
    if pending:
        return {"roll_no": roll_no, "status": "pending", "evidence": None}
    return {"roll_no": roll_no, "status": "absent", "evidence": None}

@router.get("/students")
def list_students(db: Session = Depends(get_db)):
    return [{"roll_no": s.roll_no, "name": s.name, "gallery_embedding_count": s.gallery_embedding_count}
            for s in db.query(Student).order_by(Student.roll_no).all()]

@router.get("/students/{roll_no}/gallery")
def student_gallery(roll_no: str, db: Session = Depends(get_db)):
    """Per-student view of the face gallery: what the DB actually holds, plus how
    many photos exist in the on-disk ENROLL_PHOTOS/<roll_no>/ folder. This lets a
    non-DBMS user see the state without opening SQLite."""
    roll_no = normalize_roll_no(roll_no)
    student = find_student(db, roll_no)
    if not student:
        raise HTTPException(404, "student not found")
    entries = db.query(FaceGallery).filter_by(roll_no=student.roll_no).order_by(FaceGallery.gallery_id).all()
    folder = settings.enrollment_photos_root / student.roll_no
    on_disk = sorted(p.name for p in folder.iterdir() if p.is_file()) if folder.is_dir() else []
    return {
        "roll_no": student.roll_no,
        "name": student.name,
        "enrolled_at": student.enrolled_at,
        "gallery_embedding_count": student.gallery_embedding_count,
        "db_entries": [{"gallery_id": e.gallery_id, "added_via": e.added_via,
                        "source_image_path": e.source_image_path, "added_at": e.added_at} for e in entries],
        "enrollment_photos": on_disk,
        "enrollment_photo_count": len(on_disk),
        # Drift means the cached count disagrees with the actual gallery rows, or
        # the student has no usable embedding at all. Photo-file count is reported
        # for transparency but is not itself a drift signal (a folder may hold
        # originals plus mirrored copies).
        "drift": len(entries) != student.gallery_embedding_count or len(entries) == 0,
    }

@router.get("/system/consistency")
def system_consistency(db: Session = Depends(get_db)):
    """Report every place the database and the on-disk enrollment folders have
    drifted apart, so mismatches are visible to a non-DBMS operator."""
    issues: list[dict] = []
    root = settings.enrollment_photos_root
    students = {s.roll_no: s for s in db.query(Student).all()}
    gallery_counts = {roll: n for roll, n in
                      db.query(FaceGallery.roll_no, func.count(FaceGallery.gallery_id)).group_by(FaceGallery.roll_no).all()}

    for roll, student in sorted(students.items()):
        actual = gallery_counts.get(roll, 0)
        if actual != student.gallery_embedding_count:
            issues.append({"roll_no": roll, "type": "stale_embedding_count",
                           "detail": f"students row says {student.gallery_embedding_count}, face_gallery holds {actual}"})
        if actual == 0:
            issues.append({"roll_no": roll, "type": "student_without_gallery",
                           "detail": "student exists but has no usable face embedding"})
        if not (root / roll).is_dir():
            issues.append({"roll_no": roll, "type": "student_without_photo_folder",
                           "detail": f"student exists but ENROLL_PHOTOS/{roll}/ is missing"})

    if root.is_dir():
        for folder in sorted(p for p in root.iterdir() if p.is_dir()):
            roll = normalize_roll_no(folder.name)
            photos = [p for p in folder.iterdir() if p.is_file()]
            if roll not in students:
                issues.append({"roll_no": roll, "type": "photos_without_student",
                               "detail": f"{len(photos)} photo(s) in ENROLL_PHOTOS/{folder.name} but no student row"})

    for roll, in db.query(FaceGallery.roll_no).distinct().all():
        if roll not in students:
            issues.append({"roll_no": roll, "type": "orphan_gallery_entry",
                           "detail": "face_gallery row references a missing student"})

    return {"consistent": len(issues) == 0, "issue_count": len(issues), "issues": issues}

@router.get("/session/{session_id}/absentees")
def absentees(session_id: int, db: Session = Depends(get_db)):
    if not db.get(ClassSession,session_id): raise HTTPException(404,"session not found")
    enrolled={x.roll_no for x in db.query(Student).all()}
    # Attendance is only ever 'present' for a confirmed (auto/manual_label) event.
    seen={x[0] for x in db.query(AttendanceEvent.roll_no)
          .filter(AttendanceEvent.session_id==session_id,
                  AttendanceEvent.roll_no.is_not(None),
                  AttendanceEvent.match_type.in_(CONFIRMED_MATCH_TYPES)).distinct()}
    manual=db.query(AttendanceEvent).filter_by(session_id=session_id,match_type="manual_label").count()
    return {"absentees":sorted(enrolled-seen),"summary":{"enrolled":len(enrolled),"present":len(seen),"absent":len(enrolled-seen),"manually_resolved":manual}}

@router.get("/session/{session_id}/status")
def session_status(session_id: int, db: Session = Depends(get_db)):
    report=absentees(session_id,db); pending=db.query(ReviewQueue).join(AttendanceEvent).filter(AttendanceEvent.session_id==session_id,ReviewQueue.status=="pending").count()
    return {**report["summary"],"pending":pending}

@router.post("/session/{session_id}/end")
def end_session(session_id: int, db: Session = Depends(get_db)):
    session=db.get(ClassSession,session_id)
    if not session: raise HTTPException(404,"session not found")
    if not session.end_time:
        session.end_time = datetime.now(timezone.utc)
        db.commit()
    return {"session_id":session_id,"end_time":session.end_time,"report":absentees(session_id,db)}
