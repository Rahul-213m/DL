import io
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient
from app.core.config import settings
from app.models.database import Base, engine
from app.pipeline.recognizer import DetectedFace, recognizer

def _image():
    out=io.BytesIO(); Image.new("RGB", (100,100), "white").save(out,"JPEG"); return out.getvalue()

def test_capture_review_resolve_query_flow(monkeypatch, tmp_path):
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    settings.storage_root=tmp_path; settings.high_confidence_threshold=.9; settings.low_confidence_threshold=.8
    calls={"n":0}
    def detect(_):
        calls["n"] += 1
        vector=np.array([1.,0.], dtype=np.float32) if calls["n"] <= 8 else np.array([.5,.8660254], dtype=np.float32)
        return [DetectedFace((10,10,70,70), vector, .99)]
    monkeypatch.setattr(recognizer,"detect",detect)
    from app.main import app
    with TestClient(app) as client:
        headers={"X-API-Key": settings.api_key}
        assert client.get("/session/1/status").status_code == 401
        files=[("images",("face.jpg",_image(),"image/jpeg")) for _ in range(8)]
        assert client.post("/students/enroll",data={"roll_no":"R1","name":"Ada"},files=files,headers=headers).status_code == 201
        sid=client.post("/session/start",json={"class_id":"A"},headers=headers).json()["session_id"]
        assert client.post(f"/session/{sid}/capture",files={"frame":("class.jpg",_image(),"image/jpeg")},headers=headers).status_code == 202
        queue=client.get(f"/session/{sid}/review-queue",headers=headers).json(); assert len(queue) == 1
        assert client.post(f"/review/{queue[0]['review_id']}/resolve",json={"roll_no":"R1","resolved_by":"tester"},headers=headers).status_code == 200
        response=client.get(f"/session/{sid}/query/R1",headers=headers).json()
        assert response["status"] == "present" and response["evidence"]["match_type"] == "manual_label"
        assert client.post(f"/review/{queue[0]['review_id']}/reopen",headers=headers).status_code == 200
        assert len(client.get(f"/session/{sid}/review-queue",headers=headers).json()) == 1

def test_confirm_faces_are_deduplicated_across_frames(monkeypatch, tmp_path):
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    settings.storage_root=tmp_path; settings.high_confidence_threshold=.9; settings.low_confidence_threshold=.4
    calls={"n":0}
    def detect(_):
        calls["n"] += 1
        vector=np.array([1.,0.], dtype=np.float32) if calls["n"] <= 8 else np.array([.5,.8660254], dtype=np.float32)
        return [DetectedFace((10,10,70,70), vector, .99)]
    monkeypatch.setattr(recognizer,"detect",detect)
    from app.main import app
    with TestClient(app) as client:
        headers={"X-API-Key": settings.api_key}
        files=[("images",("face.jpg",_image(),"image/jpeg")) for _ in range(8)]
        client.post("/students/enroll",data={"roll_no":"R1","name":"Ada"},files=files,headers=headers)
        sid=client.post("/session/start",json={"class_id":"A"},headers=headers).json()["session_id"]
        for _ in range(2):
            assert client.post(f"/session/{sid}/capture",files={"frame":("class.jpg",_image(),"image/jpeg")},headers=headers).status_code == 202
        assert len(client.get(f"/session/{sid}/review-queue",headers=headers).json()) == 1

def test_review_dismiss_and_reopen_flow(monkeypatch, tmp_path):
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    settings.storage_root=tmp_path; settings.high_confidence_threshold=.9; settings.low_confidence_threshold=.8
    calls={"n":0}
    def detect(_):
        calls["n"] += 1
        vector=np.array([1.,0.], dtype=np.float32) if calls["n"] <= 8 else np.array([.5,.8660254], dtype=np.float32)
        return [DetectedFace((10,10,70,70), vector, .99)]
    monkeypatch.setattr(recognizer,"detect",detect)
    from app.main import app
    with TestClient(app) as client:
        headers={"X-API-Key": settings.api_key}
        files=[("images",("face.jpg",_image(),"image/jpeg")) for _ in range(8)]
        client.post("/students/enroll",data={"roll_no":"R1","name":"Ada"},files=files,headers=headers)
        sid=client.post("/session/start",json={"class_id":"A"},headers=headers).json()["session_id"]
        client.post(f"/session/{sid}/capture",files={"frame":("class.jpg",_image(),"image/jpeg")},headers=headers)
        queue=client.get(f"/session/{sid}/review-queue",headers=headers).json()
        assert len(queue) == 1
        rid = queue[0]["review_id"]
        # Dismiss instead of resolving
        assert client.post(f"/review/{rid}/dismiss",headers=headers).status_code == 200
        # No pending items left
        assert len(client.get(f"/session/{sid}/review-queue",headers=headers).json()) == 0
        # Student count unchanged
        assert len(client.get("/students",headers=headers).json()) == 1
        # Can reopen dismissed item
        assert client.post(f"/review/{rid}/reopen",headers=headers).status_code == 200
        assert len(client.get(f"/session/{sid}/review-queue",headers=headers).json()) == 1

def test_dominant_face_enrollment(monkeypatch, tmp_path):
    Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
    settings.storage_root=tmp_path
    def detect(_):
        # 1 dominant face (area 100x100 = 10000) and 1 small face (area 40x40 = 1600) -> ratio > 6x
        return [
            DetectedFace((10,10,110,110), np.array([1.,0.], dtype=np.float32), .99),
            DetectedFace((120,120,160,160), np.array([0.,1.], dtype=np.float32), .85),
        ]
    monkeypatch.setattr(recognizer,"detect",detect)
    from app.main import app
    with TestClient(app) as client:
        headers={"X-API-Key": settings.api_key}
        files=[("images",("face.jpg",_image(),"image/jpeg")) for _ in range(8)]
        res = client.post("/students/enroll",data={"roll_no":"R2","name":"Bob"},files=files,headers=headers)
        assert res.status_code == 201
        assert res.json()["gallery_embedding_count"] == 8

