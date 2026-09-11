from datetime import datetime, timezone
import io
import logging
from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, UploadFile, status
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
async def image_bytes(upload: UploadFile) -> bytes:
    if upload.content_type not in {"image/jpeg", "image/png", "image/webp"}: raise HTTPException(415, "Only JPEG, PNG, or WebP images are accepted")
    data = await upload.read()
    if not data or len(data) > settings.max_upload_bytes: raise HTTPException(413, "Invalid or oversized image")
    try: Image.open(io.BytesIO(data)).verify()
    except Exception: raise HTTPException(422, "Upload is not a valid image")
    return data

@router.post("/students/enroll", status_code=status.HTTP_201_CREATED)
async def enroll(roll_no: str = Form(...), name: str = Form(...), images: list[UploadFile] = File(...), db: Session = Depends(get_db)):
    if not 8 <= len(images) <= 15: raise HTTPException(422, "Enrollment requires 8–15 images")
    if db.get(Student, roll_no): raise HTTPException(409, "roll number already exists")
    processed=[]
    for index, upload in enumerate(images, 1):
        data = await image_bytes(upload)
        image = np.asarray(Image.open(io.BytesIO(data)).convert("RGB"))
        try: faces = recognizer.detect(image)
        except Exception as exc: log.exception("enrollment inference failed"); raise HTTPException(503, "Face recognition model unavailable") from exc
        if len(faces) != 1: raise HTTPException(422, f"Image {index}: expected exactly one face; detected {len(faces)}")
        processed.append((data, faces[0].embedding))
    student=Student(roll_no=roll_no, name=name); db.add(student); db.flush()
    for data, embedding in processed:
        path=storage.save(data, f"enrollment/{roll_no}"); append_gallery(db, roll_no, embedding, path, "enrollment")
    db.commit()
    return {"roll_no": roll_no, "gallery_embedding_count": len(processed)}

@router.post("/students/import-folders")
def import_enrollment_folders(db: Session = Depends(get_db)):
    """Import one student per folder under ENROLL_PHOTOS_ROOT."""
    root = settings.enrollment_photos_root
    if not root.is_dir():
        raise HTTPException(404, f"Enrollment folder not found: {root}")

    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    imported, skipped = [], []
    for folder in sorted(path for path in root.iterdir() if path.is_dir()):
        roll_no = folder.name
        image_paths = sorted(path for path in folder.iterdir() if path.is_file() and path.suffix.lower() in allowed_extensions)
        if db.get(Student, roll_no):
            skipped.append({"roll_no": roll_no, "reason": "student already exists"})
            continue
        if not 8 <= len(image_paths) <= 15:
            skipped.append({"roll_no": roll_no, "reason": "requires 8–15 supported images", "image_count": len(image_paths)})
            continue

        processed = []
        try:
            for index, image_path in enumerate(image_paths, 1):
                data = image_path.read_bytes()
                if not data or len(data) > settings.max_upload_bytes:
                    raise ValueError(f"Image {index}: invalid or oversized image")
                Image.open(io.BytesIO(data)).verify()
                image = np.asarray(Image.open(io.BytesIO(data)).convert("RGB"))
                faces = recognizer.detect(image)
                if len(faces) != 1:
                    raise ValueError(f"Image {index}: expected exactly one face; detected {len(faces)}")
                processed.append((data, faces[0].embedding))
        except Exception as exc:
            log.exception("folder enrollment failed", extra={"roll_no": roll_no})
            skipped.append({"roll_no": roll_no, "reason": str(exc)})
            continue

        try:
            student = Student(roll_no=roll_no, name=roll_no)
            db.add(student)
            db.flush()
            for data, embedding in processed:
                path = storage.save(data, f"enrollment/{roll_no}")
                append_gallery(db, roll_no, embedding, path, "enrollment")
            db.commit()
            imported.append({"roll_no": roll_no, "gallery_embedding_count": len(processed)})
        except Exception as exc:
            db.rollback()
            log.exception("folder enrollment could not be saved", extra={"roll_no": roll_no})
            skipped.append({"roll_no": roll_no, "reason": f"database error: {exc}"})
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

@router.get("/session/{session_id}/review-queue")
def review_queue(session_id: int, db: Session = Depends(get_db)):
    rows=db.query(ReviewQueue, AttendanceEvent).join(AttendanceEvent).filter(AttendanceEvent.session_id==session_id, ReviewQueue.status=="pending").all()
    return [{"review_id":q.review_id,"event_id":e.event_id,"best_guess": q.proposed_roll_no,"face_crop_path":e.face_crop_path,"boxed_frame_path":bbox_context(e),"confidence_score":e.confidence_score,"captured_at":e.captured_at} for q,e in rows]

@router.post("/review/{review_id}/resolve")
def resolve(review_id: int, body: ResolveReview, db: Session = Depends(get_db)):
    queue=db.get(ReviewQueue, review_id)
    if not queue: raise HTTPException(404, "review item not found")
    if queue.status != "pending": raise HTTPException(409, "review item is already resolved")
    event=db.get(AttendanceEvent, queue.event_id)
    student=db.get(Student, body.roll_no)
    if not student:
        student=Student(roll_no=body.roll_no, name=body.name or body.roll_no); db.add(student); db.flush()
    embedding=unpack_embedding(event.embedding)
    append_gallery(db, body.roll_no, embedding, event.face_crop_path, "manual_label")
    event.roll_no = body.roll_no
    event.match_type = "manual_label"
    queue.status = "resolved"
    queue.resolved_roll_no = body.roll_no
    queue.resolved_by = body.resolved_by
    queue.resolved_at = datetime.now(timezone.utc)
    db.commit()
    return {"review_id":review_id,"roll_no":body.roll_no,"status":"resolved"}

@router.post("/review/{review_id}/reopen")
def reopen_review(review_id: int, db: Session = Depends(get_db)):
    """Undo a manual resolution and return the face to the pending review queue."""
    queue = db.get(ReviewQueue, review_id)
    if not queue:
        raise HTTPException(404, "review item not found")
    if queue.status != "resolved":
        raise HTTPException(409, "review item is not resolved")

    event = db.get(AttendanceEvent, queue.event_id)
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

    event.roll_no = None
    event.match_type = "low_conf_confirm"
    queue.status = "pending"
    queue.resolved_roll_no = None
    queue.resolved_by = None
    queue.resolved_at = None
    db.commit()
    gallery_index.rebuild(db)
    return {"review_id": review_id, "status": "pending"}

@router.get("/session/{session_id}/query/{roll_no}")
def query(session_id: int, roll_no: str, db: Session = Depends(get_db)):
    event=db.query(AttendanceEvent).filter_by(session_id=session_id,roll_no=roll_no).order_by(AttendanceEvent.confidence_score.desc()).first()
    if not event: return {"roll_no":roll_no,"status":"absent","evidence":None}
    return {"roll_no":roll_no,"status":"present","evidence":{"face_crop_path":event.face_crop_path,"full_frame_path":event.full_frame_path,"confidence_score":event.confidence_score,"match_type":event.match_type,"captured_at":event.captured_at}}

@router.get("/students")
def list_students(db: Session = Depends(get_db)):
    return [{"roll_no": s.roll_no, "name": s.name, "gallery_embedding_count": s.gallery_embedding_count}
            for s in db.query(Student).order_by(Student.roll_no).all()]

@router.get("/session/{session_id}/absentees")
def absentees(session_id: int, db: Session = Depends(get_db)):
    if not db.get(ClassSession,session_id): raise HTTPException(404,"session not found")
    enrolled={x.roll_no for x in db.query(Student).all()}; seen={x[0] for x in db.query(AttendanceEvent.roll_no).filter_by(session_id=session_id).filter(AttendanceEvent.roll_no.is_not(None)).distinct()}
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
