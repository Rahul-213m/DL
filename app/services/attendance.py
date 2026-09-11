from datetime import datetime
import io, logging
import numpy as np
from PIL import Image, ImageDraw
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.database import AttendanceEvent, ClassSession, ReviewQueue
from app.pipeline.matching import route_match, cosine_similarity
from app.pipeline.recognizer import DetectedFace, recognizer
from app.services.gallery import gallery_index, pack_embedding, unpack_embedding
from app.storage.local import storage

log = logging.getLogger(__name__)

def _jpg(image: Image.Image) -> bytes:
    out = io.BytesIO(); image.save(out, "JPEG", quality=90); return out.getvalue()

def _is_duplicate(db: Session, session_id: int, embedding: np.ndarray) -> bool:
    pending = db.query(AttendanceEvent).join(ReviewQueue).filter(AttendanceEvent.session_id == session_id, ReviewQueue.status == "pending").all()
    return any(cosine_similarity(embedding, unpack_embedding(e.embedding)) >= settings.high_confidence_threshold for e in pending)

def _iou(first: tuple[int, int, int, int], second: tuple[int, int, int, int]) -> float:
    left, top = max(first[0], second[0]), max(first[1], second[1])
    right, bottom = min(first[2], second[2]), min(first[3], second[3])
    intersection = max(0, right-left) * max(0, bottom-top)
    union = (first[2]-first[0])*(first[3]-first[1]) + (second[2]-second[0])*(second[3]-second[1]) - intersection
    return intersection / union if union else 0.0

def _detect_faces(image: np.ndarray) -> list[DetectedFace]:
    """Detect once for ordinary images; tile oversized classroom frames."""
    height, width = image.shape[:2]
    if max(height, width) <= settings.tiling_threshold_px:
        return recognizer.detect(image)
    candidates: list[DetectedFace] = list(recognizer.detect(image))
    half_h, half_w = (height + 1) // 2, (width + 1) // 2
    overlap_h, overlap_w = int(half_h * settings.tiling_overlap_ratio), int(half_w * settings.tiling_overlap_ratio)
    for y in (0, max(0, height-half_h)):
        for x in (0, max(0, width-half_w)):
            y_end, x_end = min(height, y+half_h+overlap_h), min(width, x+half_w+overlap_w)
            for face in recognizer.detect(image[y:y_end, x:x_end]):
                x1, y1, x2, y2 = face.bbox
                candidates.append(DetectedFace((x1+x, y1+y, x2+x, y2+y), face.embedding, face.detector_score))
    kept: list[DetectedFace] = []
    for candidate in sorted(candidates, key=lambda face: face.detector_score, reverse=True):
        if not any(_iou(candidate.bbox, prior.bbox) > 0.5 for prior in kept):
            kept.append(candidate)
    return kept

def process_frame(db: Session, session_id: int, content: bytes) -> int:
    if not db.get(ClassSession, session_id): raise ValueError("session not found")
    image = Image.open(io.BytesIO(content)).convert("RGB")
    frame_path = storage.save(content, f"sessions/{session_id}/frames")
    log.info("frame received", extra={"stage": "frame_received", "session_id": session_id, "frame_path": frame_path})
    faces = _detect_faces(np.asarray(image))
    log.info("faces detected", extra={"stage": "faces_detected", "session_id": session_id, "count": len(faces)})
    created = 0
    for face in faces:
        x1,y1,x2,y2 = face.bbox
        x1,y1=max(0,x1),max(0,y1); x2,y2=min(image.width,x2),min(image.height,y2)
        if x2 <= x1 or y2 <= y1: continue
        if x2-x1 < settings.min_face_size_px or y2-y1 < settings.min_face_size_px:
            log.debug("low-quality face detection discarded", extra={"session_id": session_id, "bbox": face.bbox})
            continue
        crop_path = storage.save(_jpg(image.crop((x1,y1,x2,y2))), f"sessions/{session_id}/faces")
        guess, score = gallery_index.search(face.embedding)
        result = route_match(guess, score, settings.high_confidence_threshold, settings.low_confidence_threshold)
        log.info("face match decided", extra={"stage": "match_decision", "session_id": session_id, "roll_no": result.roll_no, "score": result.score, "route": result.route})
        if result.route in {"review", "confirm"} and _is_duplicate(db, session_id, face.embedding):
            continue
        match_type = "auto" if result.route == "auto" else ("low_conf_confirm" if result.route == "confirm" else "review")
        event = AttendanceEvent(session_id=session_id, roll_no=result.roll_no if result.route == "auto" else None,
            face_crop_path=crop_path, full_frame_path=frame_path, embedding=pack_embedding(face.embedding), bbox=f"{x1},{y1},{x2},{y2}",
            confidence_score=result.score, match_type=match_type)
        db.add(event); db.flush(); created += 1
        if result.route != "auto":
            queue = ReviewQueue(event_id=event.event_id, proposed_roll_no=guess if result.route == "confirm" else None)
            db.add(queue); db.flush()
            log.info("review queue item created", extra={"stage": "review_created", "session_id": session_id, "review_id": queue.review_id, "event_id": event.event_id})
    db.commit()
    log.info("frame processing complete", extra={"stage": "summary", "session_id": session_id, "total_events_created": created})
    return created

def bbox_context(event: AttendanceEvent) -> str:
    if not event.full_frame_path:
        return ""
    context_dir = settings.storage_root / "review-context"
    cached_path = context_dir / f"event_{event.event_id}.jpg"
    if cached_path.exists():
        return str(cached_path)
    context_dir.mkdir(parents=True, exist_ok=True)
    image = Image.open(event.full_frame_path).convert("RGB")
    draw = ImageDraw.Draw(image)
    draw.rectangle(tuple(map(int, event.bbox.split(","))), outline="red", width=4)
    image.save(cached_path, "JPEG", quality=90)
    return str(cached_path)
