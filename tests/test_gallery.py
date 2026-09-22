import numpy as np
from app.models.database import Base, Student, FaceGallery, AttendanceEvent, ReviewQueue, engine, SessionLocal
from app.services.gallery import append_gallery, gallery_index

def test_incremental_gallery_update():
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    db=SessionLocal(); db.add(Student(roll_no="1", name="One")); db.commit()
    gallery_index.entries=[]; append_gallery(db,"1",np.array([1,0],dtype=np.float32),"x","manual_label"); db.commit()
    assert gallery_index.search(np.array([.9,.1],dtype=np.float32))[0] == "1"
    assert db.get(Student,"1").gallery_embedding_count == 1
    db.close()
def test_append_gallery_persists_when_faiss_add_fails(monkeypatch):
    """A FAISS failure must not discard the durable face_gallery row (DB is source of truth)."""
    import numpy as np
    import app.services.gallery as gallery_module

    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    db = SessionLocal()
    db.add(Student(roll_no="R4", name="R4")); db.commit()
    gallery_index.entries = []

    def boom(*_args, **_kwargs):
        raise ValueError("embedding dimension does not match gallery index")

    monkeypatch.setattr(gallery_module.gallery_index, "add", boom)
    append_gallery(db, "R4", np.array([1, 0], dtype=np.float32), "x", "manual_label")
    db.commit()

    assert db.query(FaceGallery).filter_by(roll_no="R4").count() == 1
    assert db.get(Student, "R4").gallery_embedding_count == 1
    db.close()


def test_review_resolution_for_new_roll_persists_across_restart(monkeypatch, tmp_path):
    """Resolving a review as an unenrolled roll number creates the student + gallery
    row, and the embedding is still searchable after FAISS is rebuilt from the DB."""
    import io
    import numpy as np
    from PIL import Image
    from fastapi.testclient import TestClient
    from app.core.config import settings
    from app.models.database import AttendanceEvent, ReviewQueue
    from app.pipeline.recognizer import DetectedFace, recognizer

    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    settings.storage_root = tmp_path
    settings.high_confidence_threshold = .9
    settings.low_confidence_threshold = .8

    calls = {"n": 0}
    def detect(_):
        calls["n"] += 1
        vec = np.array([1., 0.], dtype=np.float32) if calls["n"] <= 8 else np.array([.5, .8660254], dtype=np.float32)
        return [DetectedFace((10, 10, 70, 70), vec, .99)]
    monkeypatch.setattr(recognizer, "detect", detect)

    def image():
        out = io.BytesIO(); Image.new("RGB", (100, 100), "white").save(out, "JPEG"); return out.getvalue()

    from app.main import app
    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}
        files = [("images", ("face.jpg", image(), "image/jpeg")) for _ in range(8)]
        assert client.post("/students/enroll", data={"roll_no": "R1", "name": "Ada"}, files=files, headers=headers).status_code == 201
        sid = client.post("/session/start", json={"class_id": "A"}, headers=headers).json()["session_id"]
        client.post(f"/session/{sid}/capture", files={"frame": ("class.jpg", image(), "image/jpeg")}, headers=headers)
        queue = client.get(f"/session/{sid}/review-queue", headers=headers).json()
        assert len(queue) == 1
        rid = queue[0]["review_id"]

        # R4 has zero prior enrollment photos.
        resolved = client.post(f"/review/{rid}/resolve", json={"roll_no": "R4", "resolved_by": "tester"}, headers=headers)
        assert resolved.status_code == 200
        assert resolved.json()["gallery_embedding_count"] == 1

        # A resolution must also mirror the confirming image into ENROLL_PHOTOS/R4/
        # so the on-disk enrollment folder stays in sync with the database.
        r4_folder = settings.enrollment_photos_root / "R4"
        assert r4_folder.is_dir()
        assert len([p for p in r4_folder.iterdir() if p.is_file()]) >= 1

    db = SessionLocal()
    assert db.get(Student, "R4") is not None
    assert db.query(FaceGallery).filter_by(roll_no="R4", added_via="manual_label").count() == 1
    event = db.query(AttendanceEvent).order_by(AttendanceEvent.event_id.desc()).first()
    assert event.match_type == "manual_label" and event.roll_no == "R4"
    queue_row = db.query(ReviewQueue).order_by(ReviewQueue.review_id.desc()).first()
    assert queue_row.status == "resolved" and queue_row.resolved_roll_no == "R4"
    db.close()

    # Simulate a server restart: FAISS is rebuilt from the DB.
    gallery_index.entries = []
    db = SessionLocal()
    gallery_index.rebuild(db)
    matched, _score = gallery_index.search(np.array([.5, .8660254], dtype=np.float32))
    assert matched == "R4"
    db.close()
def test_append_gallery_rejects_degenerate_embeddings_and_blank_source():
    """Placeholder/NaN/blank-source entries must never poison the gallery or FAISS."""
    import numpy as np
    import pytest

    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    db = SessionLocal(); db.add(Student(roll_no="R1", name="One")); db.commit()

    with pytest.raises(ValueError):
        append_gallery(db, "R1", np.array([], dtype=np.float32), "path.jpg", "enrollment")
    with pytest.raises(ValueError):
        append_gallery(db, "R1", np.full(512, np.nan, dtype=np.float32), "path.jpg", "enrollment")
    with pytest.raises(ValueError):
        append_gallery(db, "R1", np.ones(512, dtype=np.float32), "  ", "enrollment")

    db.rollback()
    assert db.query(FaceGallery).filter_by(roll_no="R1").count() == 0
    assert db.get(Student, "R1").gallery_embedding_count == 0
    db.close()
