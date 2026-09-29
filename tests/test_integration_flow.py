import io

import numpy as np
from fastapi.testclient import TestClient
from PIL import Image

from app.core.config import settings
from app.models.database import SessionLocal, engine
from app.models.schema import FaceGallery, Student
from app.models.schema import LegacyBase as Base
from app.pipeline.recognizer import DetectedFace, recognizer


def _image():
    out = io.BytesIO()
    Image.new("RGB", (100, 100), "white").save(out, "JPEG")
    return out.getvalue()


def test_capture_review_resolve_query_flow(monkeypatch, tmp_path):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    settings.storage_root = tmp_path
    settings.high_confidence_threshold = 0.9
    settings.low_confidence_threshold = 0.8
    calls = {"n": 0}

    def detect(_):
        calls["n"] += 1
        vector = (
            np.array([1.0, 0.0], dtype=np.float32)
            if calls["n"] <= 8
            else np.array([0.5, 0.8660254], dtype=np.float32)
        )
        return [DetectedFace((10, 10, 70, 70), vector, 0.99)]

    monkeypatch.setattr(recognizer, "detect", detect)
    from app.main import app

    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}
        assert client.get("/session/1/status").status_code == 401
        files = [("images", ("face.jpg", _image(), "image/jpeg")) for _ in range(8)]
        assert (
            client.post(
                "/students/enroll", data={"roll_no": "R1", "name": "Ada"}, files=files, headers=headers
            ).status_code
            == 201
        )
        sid = client.post("/session/start", json={"class_id": "A"}, headers=headers).json()["session_id"]
        assert (
            client.post(
                f"/session/{sid}/capture",
                files={"frame": ("class.jpg", _image(), "image/jpeg")},
                headers=headers,
            ).status_code
            == 202
        )
        queue = client.get(f"/session/{sid}/review-queue", headers=headers).json()
        assert len(queue) == 1
        assert (
            client.post(
                f"/review/{queue[0]['review_id']}/resolve",
                json={"roll_no": "R1", "resolved_by": "tester"},
                headers=headers,
            ).status_code
            == 200
        )
        response = client.get(f"/session/{sid}/query/R1", headers=headers).json()
        assert response["status"] == "present" and response["evidence"]["match_type"] == "manual_label"
        assert client.post(f"/review/{queue[0]['review_id']}/reopen", headers=headers).status_code == 200
        assert len(client.get(f"/session/{sid}/review-queue", headers=headers).json()) == 1


def test_confirm_faces_are_deduplicated_across_frames(monkeypatch, tmp_path):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    settings.storage_root = tmp_path
    settings.high_confidence_threshold = 0.9
    settings.low_confidence_threshold = 0.4
    calls = {"n": 0}

    def detect(_):
        calls["n"] += 1
        vector = (
            np.array([1.0, 0.0], dtype=np.float32)
            if calls["n"] <= 8
            else np.array([0.5, 0.8660254], dtype=np.float32)
        )
        return [DetectedFace((10, 10, 70, 70), vector, 0.99)]

    monkeypatch.setattr(recognizer, "detect", detect)
    from app.main import app

    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}
        files = [("images", ("face.jpg", _image(), "image/jpeg")) for _ in range(8)]
        client.post("/students/enroll", data={"roll_no": "R1", "name": "Ada"}, files=files, headers=headers)
        sid = client.post("/session/start", json={"class_id": "A"}, headers=headers).json()["session_id"]
        for _ in range(2):
            assert (
                client.post(
                    f"/session/{sid}/capture",
                    files={"frame": ("class.jpg", _image(), "image/jpeg")},
                    headers=headers,
                ).status_code
                == 202
            )
        assert len(client.get(f"/session/{sid}/review-queue", headers=headers).json()) == 1


def test_global_review_queue_includes_pending_reviews_from_older_sessions(monkeypatch, tmp_path):
    """Starting another session must not hide an unresolved review from operators."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    settings.storage_root = tmp_path
    settings.high_confidence_threshold = 0.9
    settings.low_confidence_threshold = 0.8
    calls = {"n": 0}

    def detect(_):
        calls["n"] += 1
        vector = (
            np.array([1.0, 0.0], dtype=np.float32)
            if calls["n"] <= 8
            else np.array([0.5, 0.8660254], dtype=np.float32)
        )
        return [DetectedFace((10, 10, 70, 70), vector, 0.99)]

    monkeypatch.setattr(recognizer, "detect", detect)
    from app.main import app

    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}
        files = [("images", ("face.jpg", _image(), "image/jpeg")) for _ in range(8)]
        client.post("/students/enroll", data={"roll_no": "R1", "name": "Ada"}, files=files, headers=headers)
        first_session = client.post("/session/start", json={"class_id": "A"}, headers=headers).json()[
            "session_id"
        ]
        client.post(
            f"/session/{first_session}/capture",
            files={"frame": ("class.jpg", _image(), "image/jpeg")},
            headers=headers,
        )
        client.post("/session/start", json={"class_id": "B"}, headers=headers)

        queue = client.get("/review-queue", headers=headers).json()
        assert len(queue) == 1
        assert queue[0]["session_id"] == first_session


def test_review_dismiss_and_reopen_flow(monkeypatch, tmp_path):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    settings.storage_root = tmp_path
    settings.high_confidence_threshold = 0.9
    settings.low_confidence_threshold = 0.8
    calls = {"n": 0}

    def detect(_):
        calls["n"] += 1
        vector = (
            np.array([1.0, 0.0], dtype=np.float32)
            if calls["n"] <= 8
            else np.array([0.5, 0.8660254], dtype=np.float32)
        )
        return [DetectedFace((10, 10, 70, 70), vector, 0.99)]

    monkeypatch.setattr(recognizer, "detect", detect)
    from app.main import app

    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}
        files = [("images", ("face.jpg", _image(), "image/jpeg")) for _ in range(8)]
        client.post("/students/enroll", data={"roll_no": "R1", "name": "Ada"}, files=files, headers=headers)
        sid = client.post("/session/start", json={"class_id": "A"}, headers=headers).json()["session_id"]
        client.post(
            f"/session/{sid}/capture", files={"frame": ("class.jpg", _image(), "image/jpeg")}, headers=headers
        )
        queue = client.get(f"/session/{sid}/review-queue", headers=headers).json()
        assert len(queue) == 1
        rid = queue[0]["review_id"]
        # Dismiss instead of resolving
        assert client.post(f"/review/{rid}/dismiss", headers=headers).status_code == 200
        # No pending items left
        assert len(client.get(f"/session/{sid}/review-queue", headers=headers).json()) == 0
        # Student count unchanged
        assert len(client.get("/students", headers=headers).json()) == 1
        # Can reopen dismissed item
        assert client.post(f"/review/{rid}/reopen", headers=headers).status_code == 200
        assert len(client.get(f"/session/{sid}/review-queue", headers=headers).json()) == 1


def test_dominant_face_enrollment(monkeypatch, tmp_path):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    settings.storage_root = tmp_path

    def detect(_):
        # 1 dominant face (area 100x100 = 10000) and 1 small face (area 40x40 = 1600) -> ratio > 6x
        return [
            DetectedFace((10, 10, 110, 110), np.array([1.0, 0.0], dtype=np.float32), 0.99),
            DetectedFace((120, 120, 160, 160), np.array([0.0, 1.0], dtype=np.float32), 0.85),
        ]

    monkeypatch.setattr(recognizer, "detect", detect)
    from app.main import app

    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}
        files = [("images", ("face.jpg", _image(), "image/jpeg")) for _ in range(8)]
        res = client.post(
            "/students/enroll", data={"roll_no": "R2", "name": "Bob"}, files=files, headers=headers
        )
        assert res.status_code == 201
        assert res.json()["gallery_embedding_count"] == 8


def test_reenrollment_updates_database_when_enrollment_folder_is_full(monkeypatch, tmp_path):
    """The 15-file folder quota must never cap the SQLite face gallery."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    monkeypatch.setattr(settings, "storage_root", tmp_path / "data")
    monkeypatch.setattr(settings, "enrollment_photos_root", tmp_path / "ENROLL_PHOTOS")
    monkeypatch.setattr(settings, "max_enrollment_photos_per_student", 15)

    folder = settings.enrollment_photos_root / "R1"
    folder.mkdir(parents=True)
    for index in range(15):
        (folder / f"existing_{index}.jpg").write_bytes(_image())

    def detect(_):
        return [DetectedFace((10, 10, 70, 70), np.array([1.0, 0.0], dtype=np.float32), 0.99)]

    monkeypatch.setattr(recognizer, "detect", detect)

    from app.main import app

    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}
        files = [("images", ("face.jpg", _image(), "image/jpeg")) for _ in range(8)]
        first = client.post(
            "/students/enroll", data={"roll_no": "R1", "name": "Rahul"}, files=files, headers=headers
        )
        assert first.status_code == 201
        assert first.json()["gallery_embedding_count"] == 8

        second = client.post(
            "/students/enroll", data={"roll_no": "R1", "name": "Rahul"}, files=files, headers=headers
        )
        assert second.status_code == 201
        assert second.json()["gallery_embedding_count"] == 16

    db = SessionLocal()
    assert db.query(FaceGallery).filter_by(roll_no="R1").count() == 16
    db.close()
    assert len([path for path in folder.iterdir() if path.is_file()]) == 15


def _make_roll_folder(tmp_path, roll_no, count=8):
    folder = tmp_path / roll_no
    folder.mkdir(parents=True, exist_ok=True)
    for i in range(count):
        (folder / f"face_{i}.jpg").write_bytes(_image())
    return folder


def test_folder_import_updates_existing_students_and_retries_a_concurrent_insert(monkeypatch, tmp_path):
    """Folder import must append images for existing students; a concurrent create
    is retried as that same update rather than dropping its images."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    settings.storage_root = tmp_path / "data"
    settings.enrollment_photos_root = tmp_path / "ENROLL_PHOTOS"

    def detect(_):
        return [DetectedFace((10, 10, 110, 110), np.array([1.0, 0.0], dtype=np.float32), 0.99)]

    monkeypatch.setattr(recognizer, "detect", detect)

    _make_roll_folder(settings.enrollment_photos_root, "R1")
    _make_roll_folder(settings.enrollment_photos_root, "R2")
    _make_roll_folder(settings.enrollment_photos_root, "R3")

    db = SessionLocal()
    db.add(Student(roll_no="R1", name="R1"))
    db.add(Student(roll_no="R2", name="R2"))
    db.commit()
    db.close()

    from app.main import app

    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}

        # Simulate a concurrent import: R3's row appears *after* the request opens its
        # session but is present before R3's guard runs. We do this by inserting R3 from
        # a separate session partway through by patching find_student to no-op the first
        # time it is asked about R3 (mimicking a read that missed the just-committed row).
        import app.api.routes as routes

        real_find = routes.find_student
        state = {"tripped": False}

        def racing_find(session, roll_no):
            if roll_no == "R3" and not state["tripped"]:
                state["tripped"] = True
                other = SessionLocal()
                other.add(Student(roll_no="R3", name="R3"))
                other.commit()
                other.close()
                return None  # the racing read misses the row it just raced with
            return real_find(session, roll_no)

        monkeypatch.setattr(routes, "find_student", racing_find)

        res = client.post("/students/import-folders", headers=headers)
        assert res.status_code == 200
        imported = {row["roll_no"]: row for row in res.json()["imported"]}
        assert set(imported) == {"R1", "R2", "R3"}
        assert all(row["status"] == "updated" for row in imported.values())
        assert all(row["added_embedding_count"] == 8 for row in imported.values())
        assert res.json()["skipped"] == []

    db = SessionLocal()
    assert all(db.query(FaceGallery).filter_by(roll_no=roll).count() == 8 for roll in ("R1", "R2", "R3"))
    db.close()


def test_import_folders_normalizes_case_and_whitespace_variants(monkeypatch, tmp_path):
    """A case variant updates the existing student once; the duplicate folder is skipped."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    settings.storage_root = tmp_path / "data"
    settings.enrollment_photos_root = tmp_path / "ENROLL_PHOTOS"

    def detect(_):
        return [DetectedFace((10, 10, 110, 110), np.array([1.0, 0.0], dtype=np.float32), 0.99)]

    monkeypatch.setattr(recognizer, "detect", detect)

    # 'R3' (existing) and 'r3' (case variant folder) normalize to the same roll number.
    _make_roll_folder(settings.enrollment_photos_root, "R3")
    _make_roll_folder(settings.enrollment_photos_root, "r3")

    db = SessionLocal()
    db.add(Student(roll_no="R3", name="R3"))
    db.commit()
    db.close()

    from app.main import app

    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}
        res = client.post("/students/import-folders", headers=headers)
        assert res.status_code == 200
        reasons = {row["roll_no"]: row["reason"] for row in res.json()["skipped"]}
        assert len(res.json()["imported"]) == 1
        assert res.json()["imported"][0]["roll_no"] == "R3"
        assert res.json()["imported"][0]["status"] == "updated"
        assert any("duplicate folder" in reason for reason in reasons.values())

    db = SessionLocal()
    assert db.query(Student).filter_by(roll_no="R3").count() == 1
    assert db.query(FaceGallery).filter_by(roll_no="R3").count() == 8
    db.close()


def test_folder_import_updates_database_after_local_photo_cap(monkeypatch, tmp_path):
    """All valid folder images reach SQLite even when ENROLL_PHOTOS is already full."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    monkeypatch.setattr(settings, "storage_root", tmp_path / "data")
    monkeypatch.setattr(settings, "enrollment_photos_root", tmp_path / "ENROLL_PHOTOS")
    monkeypatch.setattr(settings, "max_enrollment_photos_per_student", 15)
    _make_roll_folder(settings.enrollment_photos_root, "R1", count=16)

    db = SessionLocal()
    db.add(Student(roll_no="R1", name="Rahul"))
    db.commit()
    db.close()

    def detect(_):
        return [DetectedFace((10, 10, 110, 110), np.array([1.0, 0.0], dtype=np.float32), 0.99)]

    monkeypatch.setattr(recognizer, "detect", detect)

    from app.main import app

    with TestClient(app) as client:
        response = client.post("/students/import-folders", headers={"X-API-Key": settings.api_key})
        assert response.status_code == 200
        result = response.json()["imported"]
        assert result == [
            {"roll_no": "R1", "gallery_embedding_count": 16, "added_embedding_count": 16, "status": "updated"}
        ]

    db = SessionLocal()
    assert db.query(FaceGallery).filter_by(roll_no="R1").count() == 16
    db.close()
    assert len(list((settings.enrollment_photos_root / "R1").iterdir())) == 16


def test_query_prefers_manual_label_over_higher_scoring_auto(monkeypatch, tmp_path):
    """A human correction must outrank an automatic match when surfacing evidence.

    Repro: a reviewed face is stored as manual_label with a low detection score, and a
    *different* face for the same roll number auto-matches with a higher score. The
    evidence query must return the reviewed (manual_label) event, not the auto one.
    """
    from app.models.schema import AttendanceEvent

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    settings.storage_root = tmp_path

    db = SessionLocal()
    db.add(Student(roll_no="R3", name="R3"))
    db.commit()
    from app.models.schema import ClassSession

    session = ClassSession(class_id="A")
    db.add(session)
    db.flush()
    # manual label: the reviewed face, low score
    db.add(
        AttendanceEvent(
            session_id=session.session_id,
            roll_no="R3",
            face_crop_path="data/reviewed.jpg",
            embedding=b"\x00",
            bbox="0,0,1,1",
            confidence_score=0.28,
            match_type="manual_label",
        )
    )
    # auto: a different face for the same roll, higher score
    db.add(
        AttendanceEvent(
            session_id=session.session_id,
            roll_no="R3",
            face_crop_path="data/auto_wrongface.jpg",
            embedding=b"\x00",
            bbox="0,0,1,1",
            confidence_score=0.95,
            match_type="auto",
        )
    )
    db.commit()
    sid = session.session_id
    db.close()

    from app.api.routes import query

    db = SessionLocal()
    result = query(sid, "R3", db)
    assert result["status"] == "present"
    assert result["evidence"]["match_type"] == "manual_label"
    assert result["evidence"]["face_crop_path"] == "data/reviewed.jpg"
    db.close()


def test_query_absent_when_roll_has_no_events(monkeypatch, tmp_path):
    from app.models.schema import ClassSession

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    session = ClassSession(class_id="A")
    db.add(session)
    db.commit()
    sid = session.session_id
    db.close()

    from app.api.routes import query

    db = SessionLocal()
    assert query(sid, "R9", db) == {"roll_no": "R9", "status": "absent", "evidence": None}
    db.close()


def test_query_does_not_claim_present_for_unconfirmed_auto(monkeypatch, tmp_path):
    """A student whose only event is an unconfirmed review draft must not be shown
    as present — the API reports 'pending', never a false 'present'."""
    from app.models.schema import AttendanceEvent, ClassSession, ReviewQueue

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    db = SessionLocal()
    db.add(Student(roll_no="R7", name="R7"))
    db.commit()
    session = ClassSession(class_id="A")
    db.add(session)
    db.flush()
    # The capture pipeline keeps roll_no empty until confirmation; the proposed
    # candidate is stored on ReviewQueue instead.
    ev = AttendanceEvent(
        session_id=session.session_id,
        roll_no=None,
        face_crop_path="x.jpg",
        embedding=b"\x00",
        bbox="0,0,1,1",
        confidence_score=0.4,
        match_type="low_conf_confirm",
    )
    db.add(ev)
    db.flush()
    db.add(ReviewQueue(event_id=ev.event_id, proposed_roll_no="R7", status="pending"))
    db.commit()
    sid = session.session_id
    db.close()

    from app.api.routes import absentees, query

    db = SessionLocal()
    assert query(sid, "R7", db)["status"] == "pending"
    # and it must not count toward present
    assert "R7" in absentees(sid, db)["absentees"]
    db.close()


def test_system_consistency_and_repair(monkeypatch, tmp_path):
    """The consistency endpoint reports drift and repair reconciles the counts."""
    import numpy as np

    from app.services.gallery import append_gallery

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    settings.storage_root = tmp_path / "data"
    settings.enrollment_photos_root = tmp_path / "ENROLL_PHOTOS"

    db = SessionLocal()
    db.add(Student(roll_no="R9", name="R9"))
    db.commit()
    append_gallery(db, "R9", np.array([1.0, 0.0], dtype=np.float32), "a.jpg", "enrollment")
    db.commit()
    # Corrupt the cached count to simulate drift.
    db.get(Student, "R9").gallery_embedding_count = 5
    db.commit()
    db.close()

    from app.main import app

    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}
        report = client.get("/system/consistency", headers=headers).json()
        assert report["consistent"] is False
        assert any(i["type"] == "stale_embedding_count" for i in report["issues"])

        repaired = client.post("/system/repair", headers=headers).json()
        assert repaired["repaired_count"] == 1
        assert client.get("/system/consistency", headers=headers).json()["consistent"] is True


def test_reimport_rebuilds_gallery_from_enroll_photos(monkeypatch, tmp_path):
    """Re-import rebuilds a student with no gallery from ENROLL_PHOTOS/<roll>/."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    settings.storage_root = tmp_path / "data"
    settings.enrollment_photos_root = tmp_path / "ENROLL_PHOTOS"

    def detect(_):
        return [DetectedFace((10, 10, 110, 110), np.array([1.0, 0.0], dtype=np.float32), 0.99)]

    monkeypatch.setattr(recognizer, "detect", detect)

    folder = settings.enrollment_photos_root / "R5"
    folder.mkdir(parents=True)
    for i in range(8):
        (folder / f"f{i}.jpg").write_bytes(_image())

    from app.main import app

    with TestClient(app) as client:
        headers = {"X-API-Key": settings.api_key}
        res = client.post("/students/R5/reimport", headers=headers)
        assert res.status_code == 200
        assert res.json()["gallery_embedding_count"] == 8

    db = SessionLocal()
    assert db.get(Student, "R5") is not None
    assert db.query(FaceGallery).filter_by(roll_no="R5").count() == 8
    db.close()
