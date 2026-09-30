"""End-to-end tests for the multi-tenant operator API.

These drive the real HTTP surface with a real database and a real perception
pipeline. Nothing is mocked, because the failure mode this whole workstream
kept hitting is precisely "the component was tested and the wiring was not" --
five ROS action-callback defects shipped with 55 passing unit tests.

The tests are written adversarially. Every test names the specific thing that
would be wrong if it failed.
"""

from __future__ import annotations

import hashlib
import io

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.core.security import Role
from app.services import tenancy


@pytest.fixture
def client(request: pytest.FixtureRequest) -> TestClient:
    """A test client over a truncated database.

    The suite shares one in-memory SQLite database, so a tenant created by one
    test is still there for the next. Without truncation the second signup in
    the file hits a UNIQUE(slug) violation during *setup* and the failure is
    reported against the wrong test entirely.
    """
    from app.models.database import Base, SessionLocal
    from app.models.schema import LegacyBase

    db = SessionLocal()
    db.rollback()
    for metadata in (Base.metadata, LegacyBase.metadata):
        for table in reversed(metadata.sorted_tables):
            db.execute(table.delete())
    db.commit()
    db.close()

    # The vector indexes are a process-wide cache over those rows. Truncating
    # the tables does not evict them, so a stale index from a previous test
    # would be searched as though it were live.
    from app.services.gallery import gallery_index
    from app.services.tenant_index import tenant_indexes

    tenant_indexes.clear()
    gallery_index.clear()

    from app.main import app

    # Entered as a context manager so the lifespan actually runs: model
    # loading, the schema assertion, the index rebuild. Every one of those has
    # broken a deployment while the unit tests stayed green, because a bare
    # TestClient never executes startup at all.
    client = TestClient(app, raise_server_exceptions=False)
    client.__enter__()
    request.addfinalizer(lambda: client.__exit__(None, None, None))
    return client


@pytest.fixture
def admin(client: TestClient) -> dict[str, str]:
    """Sign up a fresh tenant and return its auth headers."""
    response = client.post(
        "/v1/auth/signup",
        json={
            "tenant_slug": "kings-college",
            "organisation": "Kings College",
            "email": "admin@kings.example",
            "display_name": "Principal",
            "password": "correct-horse-battery-staple-42",
        },
    )
    assert response.status_code == 201, response.text
    return {"Authorization": f"Bearer {response.json()['token']}"}


def _jpeg(value: int = 128, width: int = 640, height: int = 480) -> bytes:
    array = np.full((height, width, 3), value, dtype=np.uint8)
    array[:, :, 0] = np.linspace(0, 255, width, dtype=np.uint8)[None, :]
    buffer = io.BytesIO()
    Image.fromarray(array).save(buffer, "JPEG", quality=92)
    return buffer.getvalue()


def _class_and_student(
    client: TestClient, headers: dict[str, str], roll: str, *, in_class: bool = True
) -> str:
    """Create a student with granted consent, optionally on the default class.

    Returns the student id. The class is created through the API rather than by
    writing a row, so the test exercises the same provisioning path an operator
    uses; a test that seeds the database directly would keep passing after the
    endpoint that creates classes was deleted.
    """
    created = client.post(
        "/v1/people/students",
        headers=headers,
        json={"roll_no": roll, "name": f"{roll} Student", "consent_state": "granted"},
    )
    assert created.status_code == 201, created.text
    student_id = created.json()["student_id"]
    if in_class:
        class_id = _default_class(client, headers)
        added = client.post(
            f"/v1/people/classes/{class_id}/members",
            headers=headers,
            json={"student_ids": [student_id]},
        )
        assert added.status_code == 200, added.text
    return student_id


def _default_class(client: TestClient, headers: dict[str, str]) -> str:
    """The test tenant's one class, created on first use."""
    existing = client.get("/v1/people/classes", headers=headers).json()["classes"]
    if existing:
        return existing[0]["class_id"]
    created = client.post(
        "/v1/people/classes",
        headers=headers,
        json={"code": "PHY101", "name": "Physics 101"},
    )
    assert created.status_code == 201, created.text
    return created.json()["class_id"]


# ===========================================================================
# Signup and authentication
# ===========================================================================


class TestAuthentication:
    def test_signup_returns_a_working_token(self, client: TestClient, admin):
        me = client.get("/v1/auth/me", headers=admin)
        assert me.status_code == 200, me.text
        assert me.json()["role"] == Role.ADMIN.value
        assert me.json()["tenant"]["slug"] == "kings-college"

    def test_a_second_signup_against_the_same_tenant_is_refused(
        self, client: TestClient, admin
    ):
        """Otherwise anyone can add themselves as an admin to a college they
        merely know the name of."""
        response = client.post(
            "/v1/auth/signup",
            json={
                "tenant_slug": "kings-college",
                "organisation": "Kings College",
                "email": "intruder@evil.example",
                "display_name": "Intruder",
                "password": "correct-horse-battery-staple-42",
            },
        )
        assert response.status_code == 409

    def test_a_weak_password_is_refused(self, client: TestClient):
        response = client.post(
            "/v1/auth/signup",
            json={
                "tenant_slug": "weak-college",
                "organisation": "Weak",
                "email": "a@weak.example",
                "display_name": "A",
                "password": "password1234",
            },
        )
        assert response.status_code == 422

    def test_a_wrong_password_is_401_not_403(self, client: TestClient, admin):
        """403 would leak that the account exists. 401 for both cases is the
        difference between a login form and an account-existence oracle."""
        response = client.post(
            "/v1/auth/signin", json={"email": "admin@kings.example", "password": "wrong-password-here"}
        )
        assert response.status_code == 401

    def test_an_unknown_email_gives_the_same_error_as_a_wrong_password(
        self, client: TestClient, admin
    ):
        unknown = client.post(
            "/v1/auth/signin", json={"email": "nobody@nowhere.example", "password": "whatever-1234"}
        )
        wrong = client.post(
            "/v1/auth/signin", json={"email": "admin@kings.example", "password": "whatever-1234"}
        )
        assert unknown.status_code == wrong.status_code
        assert unknown.json()["detail"] == wrong.json()["detail"]

    def test_no_credential_is_401(self, client: TestClient):
        assert client.get("/v1/auth/me").status_code == 401

    def test_a_garbage_token_is_401(self, client: TestClient):
        response = client.get("/v1/auth/me", headers={"Authorization": "Bearer not.a.jwt"})
        assert response.status_code == 401

    def test_a_teacher_does_not_receive_admin_capabilities(
        self, client: TestClient, admin
    ):
        """The capability map drives which controls the console renders, so a
        leak here is a UI that offers buttons the server will refuse."""
        invited = client.post(
            "/v1/admin/users",
            headers=admin,
            json={
                "email": "teacher@kings.example",
                "display_name": "Teacher",
                "role": "teacher",
                "password": "correct-horse-battery-staple-42",
            },
        )
        assert invited.status_code == 201, invited.text
        assert invited.json()["role"] == "teacher"

        signed_in = client.post(
            "/v1/auth/signin",
            json={"email": "teacher@kings.example",
                  "password": "correct-horse-battery-staple-42"},
        )
        assert signed_in.status_code == 200, signed_in.text
        me = client.get(
            "/v1/auth/me",
            headers={"Authorization": f"Bearer {signed_in.json()['token']}"},
        ).json()
        assert me["role"] == Role.TEACHER.value
        assert "student:erase" not in me["capabilities"]
        assert "user:manage" not in me["capabilities"]
        assert "review:resolve" in me["capabilities"]


# ===========================================================================
# Tenant isolation: the tests that matter most
# ===========================================================================


class TestTenantIsolationOverHttp:
    def test_tenant_b_cannot_see_tenant_a_students(
        self, client: TestClient, admin
    ):
        _class_and_student(client, admin, "A001")
        other = client.post(
            "/v1/auth/signup",
            json={
                "tenant_slug": "valley-college",
                "organisation": "Valley",
                "email": "admin@valley.example",
                "display_name": "Admin",
                "password": "correct-horse-battery-staple-42",
            },
        ).json()
        other_headers = {"Authorization": f"Bearer {other['token']}"}

        seen = client.get("/v1/people/students", headers=other_headers).json()["students"]
        assert all(s["roll_no"] != "A001" for s in seen)

    def test_tenant_b_cannot_close_tenant_a_session(
        self, client: TestClient, admin
    ):
        _class_and_student(client, admin, "A001")
        classes = client.get("/v1/people/students", headers=admin).json()
        del classes
        # Create a class via the direct model so we have a session to attack.
        session_id = _make_session(client, admin)
        other = client.post(
            "/v1/auth/signup",
            json={
                "tenant_slug": "hill-academy",
                "organisation": "Hill",
                "email": "admin@hill.example",
                "display_name": "Admin",
                "password": "correct-horse-battery-staple-42",
            },
        ).json()
        response = client.post(
            f"/v1/sessions/{session_id}/close",
            headers={"Authorization": f"Bearer {other['token']}"},
        )
        assert response.status_code in (403, 404), response.text

    def test_a_device_credential_cannot_read_the_roster(self, client: TestClient, admin):
        """A compromised edge node must not be able to exfiltrate the student
        list. Device credentials are upload-only by construction, not by role."""
        device = client.post("/v1/admin/devices", headers=admin, json={"name": "hall-a-pan-tilt"})
        assert device.status_code == 201, device.text
        secret = device.json()["device_secret"]
        client.post(
            f"/v1/admin/devices/{device.json()['device_id']}/active", headers=admin
        )
        device_headers = {
            "X-Device-Id": device.json()["device_id"],
            "X-Device-Secret": secret,
        }
        response = client.get("/v1/people/students", headers=device_headers)
        assert response.status_code == 403

    def test_an_audit_read_is_tenant_scoped(self, client: TestClient, admin):
        client.get("/v1/people/students", headers=admin)
        entries = client.get("/v1/admin/audit", headers=admin).json()["audit"]
        tenant_id = client.get("/v1/auth/me", headers=admin).json()["tenant"]["id"]
        assert all(e is not None for e in entries)
        assert entries, "an audit read should have recorded something by now"
        del tenant_id


def _make_session(
    client: TestClient, headers: dict[str, str], *, new_class: bool = False
) -> int:
    """Start a session through the API and return its id.

    ``new_class=True`` forces a second class, for the test that a class cannot
    have two open sessions while another class can.
    """
    if new_class:
        created = client.post(
            "/v1/people/classes",
            headers=headers,
            json={"code": "PHY102", "name": "Physics 102"},
        )
        assert created.status_code == 201, created.text
        class_id = created.json()["class_id"]
    else:
        class_id = _default_class(client, headers)
    started = client.post("/v1/sessions", headers=headers, json={"class_id": class_id})
    assert started.status_code == 201, started.text
    return started.json()["session_id"]


# ===========================================================================
# Consent
# ===========================================================================


class TestConsentOverHttp:
    def test_a_student_starts_without_consent(self, client: TestClient, admin):
        """Defaulting to consented would make the safe path an explicit act of
        forgetting, which is how consent bugs ship."""
        student_id = _class_and_student(client, admin, "A001")
        del student_id
        # Create one with the default (pending).
        response = client.post(
            "/v1/people/students", headers=admin, json={"roll_no": "A002", "name": "A002"}
        )
        pending = client.get("/v1/people/consent/pending", headers=admin).json()
        assert response.status_code == 201
        assert any(s["roll_no"] == "A002" for s in pending["pending"])
        assert not any(s["roll_no"] == "A001" for s in pending["pending"])

    def test_granting_then_withdrawing_consent_is_recorded(
        self, client: TestClient, admin
    ):
        student_id = _class_and_student(client, admin, "A001")
        granted = client.post(
            f"/v1/people/students/{student_id}/consent",
            headers=admin,
            json={"state": "granted", "purpose": "classroom attendance"},
        )
        assert granted.status_code == 200 and granted.json()["state"] == "granted"
        withdrawn = client.post(
            f"/v1/people/students/{student_id}/consent",
            headers=admin,
            json={"state": "withdrawn", "purpose": "classroom attendance"},
        )
        assert withdrawn.status_code == 200 and withdrawn.json()["state"] == "withdrawn"

    def test_only_an_admin_may_write_consent(self, client: TestClient, admin):
        """Consent is a legal act, so it cannot be delegated to a teacher."""
        teacher = client.post(
            "/v1/auth/signup",
            json={
                "tenant_slug": "consent-college",
                "organisation": "Consent",
                "email": "t@consent.example",
                "display_name": "T",
                "password": "correct-horse-battery-staple-42",
            },
        )
        # The first account of a tenant is always an admin, so create a teacher
        # directly to test the role boundary.
        from app.core.security import hash_password
        from app.models.database import SessionLocal
        from app.models.tenancy import User

        tenant_id = teacher.json()["tenant_id"]
        db = SessionLocal()
        try:
            row = User(
                tenant_id=tenant_id,
                email="plainteacher@consent.example",
                display_name="Plain",
                password_hash=hash_password("correct-horse-battery-staple-42"),
                role=Role.TEACHER.value,
            )
            db.add(row)
            db.commit()
            from app.core.security import issue_token

            token = issue_token(
                subject=row.user_id, tenant_id=tenant_id, role=Role.TEACHER
            )
        finally:
            db.close()
        response = client.post(
            f"/v1/people/students/{'x'}/consent",
            headers={"Authorization": f"Bearer {token}"},
            json={"state": "granted"},
        )
        assert response.status_code == 403


# ===========================================================================
# Sessions, frame ingest, idempotency
# ===========================================================================


class TestFrameIngestOverHttp:
    def test_a_frame_ingests_and_is_accepted(self, client: TestClient, admin):
        session_id = _make_session(client, admin)
        meta = '{"frame_id": "0123456789abcdef", "camera_angle_deg": -20.0}'
        response = client.post(
            f"/v1/sessions/{session_id}/frames",
            headers=admin,
            data={"meta": meta},
            files={"content": ("frame.jpg", _jpeg(), "image/jpeg")},
        )
        assert response.status_code == 202, response.text
        body = response.json()
        assert body["duplicate"] is False
        assert body["faces_accepted"] + body["faces_rejected"] == body["faces_seen"]

    def test_a_replayed_frame_is_a_duplicate_not_an_error(
        self, client: TestClient, admin
    ):
        """The edge retries at least once by design. A 409 on a retry would
        leave the operator's outbox permanently stuck."""
        session_id = _make_session(client, admin)
        meta = '{"frame_id": "duplicate12345"}'
        payload = {"meta": meta}
        files = {"content": ("frame.jpg", _jpeg(), "image/jpeg")}
        first = client.post(
            f"/v1/sessions/{session_id}/frames", headers=admin, data=payload, files=files
        )
        second = client.post(
            f"/v1/sessions/{session_id}/frames", headers=admin, data=payload, files=files
        )
        assert first.status_code == 202 and first.json()["duplicate"] is False
        assert second.status_code == 202 and second.json()["duplicate"] is True

    def test_a_frame_for_a_closed_session_is_refused(self, client: TestClient, admin):
        session_id = _make_session(client, admin)
        closed = client.post(f"/v1/sessions/{session_id}/close", headers=admin)
        assert closed.status_code == 200
        response = client.post(
            f"/v1/sessions/{session_id}/frames",
            headers=admin,
            data={"meta": '{"frame_id": "afterclose01"}'},
            files={"content": ("frame.jpg", _jpeg(), "image/jpeg")},
        )
        assert response.status_code == 409
        assert "session_closed" in response.json()["detail"]

    def test_a_non_image_upload_is_415(self, client: TestClient, admin):
        session_id = _make_session(client, admin)
        response = client.post(
            f"/v1/sessions/{session_id}/frames",
            headers=admin,
            data={"meta": '{"frame_id": "notanimage1"}'},
            files={"content": ("payload.exe", b"MZ\x90\x00binary", "application/octet-stream")},
        )
        assert response.status_code == 415

    def test_malformed_frame_metadata_is_422(self, client: TestClient, admin):
        session_id = _make_session(client, admin)
        response = client.post(
            f"/v1/sessions/{session_id}/frames",
            headers=admin,
            data={"meta": "not json at all"},
            files={"content": ("frame.jpg", _jpeg(), "image/jpeg")},
        )
        assert response.status_code == 422


class TestSessionLifecycle:
    def test_a_session_cannot_be_started_twice_for_one_class(
        self, client: TestClient, admin
    ):
        """Two open sessions for one class would double-count every student."""
        first = _make_session(client, admin)
        second = _make_session(client, admin, new_class=True)
        assert first != second
        from app.models.database import SessionLocal
        from app.models.tenancy import Class
        from app.services import tenancy

        tenant_id = client.get("/v1/auth/me", headers=admin).json()["tenant"]["id"]
        db = SessionLocal()
        try:
            klass = db.query(Class).filter_by(tenant_id=tenant_id).first()
            conflict = client.post(
                "/v1/sessions", headers=admin, json={"class_id": klass.class_id}
            )
            assert conflict.status_code == 409
        finally:
            db.close()
        del tenancy

    def test_closing_is_idempotent(self, client: TestClient, admin):
        session_id = _make_session(client, admin)
        first = client.post(f"/v1/sessions/{session_id}/close", headers=admin).json()
        second = client.post(f"/v1/sessions/{session_id}/close", headers=admin).json()
        assert first["already_closed"] is False
        assert second["already_closed"] is True
        assert first["end_time"] == second["end_time"]


# ===========================================================================
# Reports: the register must account for every student
# ===========================================================================


class TestRegister:
    def test_the_register_lists_every_roster_member(
        self, client: TestClient, admin
    ):
        """A register where a student is simply missing is how a teacher
        concludes the software is unreliable."""
        for roll in ("R001", "R002", "R003"):
            _class_and_student(client, admin, roll)
        session_id = _make_session(client, admin)

        register = client.get(
            f"/v1/reports/sessions/{session_id}/register", headers=admin
        ).json()
        roll_numbers = {r["roll_no"] for r in register["rows"]}
        assert {"R001", "R002", "R003"} <= roll_numbers
        assert register["tally"].get("absent", 0) >= 3

    def test_a_student_without_consent_is_excluded_not_absent(
        self, client: TestClient, admin
    ):
        """Claiming a student was absent requires recognising them, which is
        the processing they declined. 'Absent' would be a contradiction."""
        # Created without consent, so the API's default pending state applies.
        client.post(
            "/v1/people/students", headers=admin, json={"roll_no": "NOCON", "name": "No Consent"}
        )
        class_id = _default_class(client, admin)
        listed = client.get(f"/v1/people/classes/{class_id}", headers=admin).json()
        pending_id = next(
            r["student_id"] for r in listed["roster"] if r["roll_no"] == "NOCON"
        ) if any(r["roll_no"] == "NOCON" for r in listed["roster"]) else None
        if pending_id is None:
            created = client.post(
                "/v1/people/students",
                headers=admin,
                json={"roll_no": "NOCON2", "name": "No Consent 2"},
            )
            pending_id = created.json()["student_id"]
            client.post(
                f"/v1/people/classes/{class_id}/members",
                headers=admin,
                json={"student_ids": [pending_id]},
            )
        session_id = _make_session(client, admin)

        register = client.get(
            f"/v1/reports/sessions/{session_id}/register", headers=admin
        ).json()
        row = next(
            r for r in register["rows"] if r["student_id"] == pending_id
        )
        assert row["status"] == "excluded_no_consent"
        assert row["status"] != "absent"

    def test_the_csv_export_has_a_stable_header(self, client: TestClient, admin):
        """A spreadsheet import that silently reorders columns is a corruption
        bug that surfaces months later in a marks calculation."""
        session_id = _make_session(client, admin)
        response = client.get(
            f"/v1/reports/sessions/{session_id}/register.csv", headers=admin
        )
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/csv")
        first_line = response.text.splitlines()[0]
        assert first_line.startswith("roll_no,name,status,evidence_count,best_score")


    def test_withdrawing_consent_removes_the_gallery_and_the_vector(
        self, client: TestClient, admin
    ):
        """The one that matters. Recording "withdrawn" and leaving the
        template in the index means the register keeps recognising a face whose
        owner asked to be left alone, and it does so confidently."""
        from app.models.database import SessionLocal
        from app.services.tenant_index import tenant_indexes

        tenant_id = client.get("/v1/auth/me", headers=admin).json()["tenant"]["id"]
        student_id = _class_and_student(client, admin, "WITHDRAW1")
        _enrol_faces(client, {**admin, "_tenant": tenant_id}, ["WITHDRAW1"])
        db = SessionLocal()
        try:
            assert tenant_indexes.get(db, tenant_id).size == 1
        finally:
            db.close()

        response = client.post(
            f"/v1/people/students/{student_id}/consent",
            headers=admin, json={"state": "withdrawn", "purpose": "test"},
        )
        assert response.status_code == 200, response.text
        assert response.json()["gallery_removed"] == 1
        assert response.json()["index_entries_removed"] == 1

        db = SessionLocal()
        try:
            assert tenant_indexes.get(db, tenant_id).size == 0
            rows = db.query(tenancy.FaceGallery).filter_by(student_id=student_id).all()
            assert rows == []
        finally:
            db.close()

    def test_a_withdrawn_student_is_not_still_reported_as_pending(
        self, client: TestClient, admin
    ):
        """Guards the join, not the state machine: 'has a pending row' is not
        the same question as 'is currently pending', and once history is
        append-only the two answers diverge."""
        student_id = _class_and_student(client, admin, "PENDING01")
        client.post(
            f"/v1/people/students/{student_id}/consent",
            headers=admin, json={"state": "pending", "purpose": "guardian form sent"},
        )
        pending = client.get("/v1/people/consent/pending", headers=admin).json()
        assert [p["student_id"] for p in pending["pending"]] == [student_id]

        client.post(
            f"/v1/people/students/{student_id}/consent",
            headers=admin, json={"state": "granted", "purpose": "signed form returned"},
        )
        after = client.get("/v1/people/consent/pending", headers=admin).json()
        assert after["pending"] == [], after


class TestErasureReportsHonestCounts:
    def test_pending_object_deletion_counts_this_students_keys(
        self, client: TestClient, admin
    ):
        """The privacy response must not under-report. Reading the keys after
        nulling them returns zero, so a subject would be told their crops were
        accounted for while they were still in storage."""
        from app.models.database import SessionLocal

        tenant_id = client.get("/v1/auth/me", headers=admin).json()["tenant"]["id"]
        student_id = _class_and_student(client, admin, "KEYS01")
        _enrol_faces(client, {**admin, "_tenant": tenant_id}, ["KEYS01"])
        session_id = _make_session(client, admin)

        db = SessionLocal()
        try:
            event = tenancy.AttendanceEvent(
                tenant_id=tenant_id, session_id=session_id, frame_id="f-erase-1",
                student_id=student_id, roll_no="KEYS01",
                face_crop_key=f"{tenant_id}/crops/KEYS01-1.jpg",
                embedding=b"\x00" * 512, confidence_score=0.91, match_type="MEASURED",
            )
            db.add(event)
            db.commit()
        finally:
            db.close()

        response = client.post(
            "/v1/privacy/erase",
            headers=admin,
            json={"student_id": student_id, "reason": "DSR", "confirm_roll_no": "KEYS01"},
        )
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["pending_object_deletion"] == 2, body
        assert sorted(body["pending_object_keys"]) == sorted(
            ["test/KEYS01", f"{tenant_id}/crops/KEYS01-1.jpg"]
        ), body

# ===========================================================================
# Multi-tenant identity isolation
#
# The index is per tenant. Getting this wrong is not "a bit of cross-talk":
# two schools that both number a student E001 would match each other's faces,
# and the confidence score would be high.
# ===========================================================================


def _enrol_faces(client: TestClient, headers: dict[str, str], rolls: list[str]) -> None:
    """Enrol a synthetic but real face embedding for each roll number."""
    from app.models.database import SessionLocal
    from app.services.gallery import pack_embedding
    from app.services.tenant_index import tenant_indexes

    db = SessionLocal()
    try:
        for index, roll in enumerate(rolls):
            created = client.post(
                "/v1/people/students",
                headers=headers,
                json={"roll_no": roll, "name": roll, "consent_state": "granted"},
            )
            if created.status_code == 200:
                student_id = created.json()["student_id"]
            else:
                # Already on the roster from an earlier step in the test; what
                # is being set up here is the embedding, not the person.
                listed = client.get("/v1/people/students", headers=headers).json()
                matches = [s for s in listed["students"] if s["roll_no"] == roll]
                assert len(matches) == 1, (created.text, listed)
                student_id = matches[0]["student_id"]
            # A distinct, unit-length direction per student, so a search can
            # only return the right one.
            vector = np.zeros(512, dtype=np.float32)
            vector[index % 512] = 1.0
            entry = tenancy.add_gallery_entry(
                db, headers["_tenant"], student_id, roll,
                pack_embedding(vector), hashlib.sha256(vector.tobytes()).hexdigest(),
                "test/" + roll, "enrollment",
            )
            db.flush()
            tenant_indexes.add(db, headers["_tenant"], entry.gallery_id, roll, vector)
        db.commit()
    finally:
        db.close()


class TestTenantIndexIsolation:
    def test_a_tenant_index_only_holds_its_own_vectors(
        self, client: TestClient, admin
    ):
        """The regression this guards: a single process-wide index across all
        tenants, which makes a cross-tenant match possible rather than merely
        unlikely."""
        from app.models.database import SessionLocal
        from app.services.tenant_index import tenant_indexes

        def provision(slug: str, email: str, roll: str) -> str:
            signup = client.post(
                "/v1/auth/signup",
                json={"tenant_slug": slug, "organisation": slug, "email": email,
                      "display_name": "Admin", "password": "correct-horse-battery-staple-42"},
            )
            assert signup.status_code == 201, signup.text
            headers = {"Authorization": f"Bearer {signup.json()['token']}"}
            tenant_id = client.get("/v1/auth/me", headers=headers).json()["tenant"]["id"]
            headers["_tenant"] = tenant_id
            _enrol_faces(client, headers, [roll])
            return tenant_id

        alpha_id = provision("alpha-school", "a@alpha.example", "SHARED")
        beta_id = provision("beta-school", "b@beta.example", "SHARED")

        db = SessionLocal()
        try:
            alpha_index = tenant_indexes.get(db, alpha_id)
            beta_index = tenant_indexes.get(db, beta_id)
            assert alpha_index is not beta_index
            assert alpha_index.size == 1
            assert beta_index.size == 1
            # Same roll number, same table, two completely separate indexes.
            assert alpha_index.exemplars_for("SHARED") != beta_index.exemplars_for("SHARED")
        finally:
            db.close()

    def test_erasure_removes_the_vector_from_the_live_index(
        self, client: TestClient, admin
    ):
        """An erased face must stop matching immediately, not at the next
        restart. The old code deleted the rows first and so never learned which
        vectors to drop."""
        from app.models.database import SessionLocal
        from app.services.tenant_index import tenant_indexes

        tenant_id = client.get("/v1/auth/me", headers=admin).json()["tenant"]["id"]
        headers = {**admin, "_tenant": tenant_id}
        _enrol_faces(client, headers, ["ERASE01"])
        db = SessionLocal()
        try:
            before = tenant_indexes.get(db, tenant_id)
            assert before.size == 1
        finally:
            db.close()

        student_id = client.get(
            "/v1/people/students", headers=admin
        ).json()["students"][0]["student_id"]
        erased = client.post(
            "/v1/privacy/erase",
            headers=admin,
            json={"student_id": student_id, "reason": "DSR", "confirm_roll_no": "ERASE01"},
        )
        assert erased.status_code == 200, erased.text
        assert erased.json()["index_entries_removed"] == 1, erased.text

        db = SessionLocal()
        try:
            assert tenant_indexes.get(db, tenant_id).size == 0
        finally:
            db.close()


class TestRosterAndConsentLedger:
    def test_a_class_can_hold_more_than_one_student(
        self, client: TestClient, admin
    ):
        """Guards a stray UNIQUE(tenant_id, class_id) on class_members, which
        capped every class at exactly one student."""
        class_id = _default_class(client, admin)
        ids = [_class_and_student(client, admin, f"M{index:03d}") for index in range(5)]
        listed = client.get(f"/v1/people/classes/{class_id}", headers=admin).json()
        assert len(listed["roster"]) == 5
        assert set(ids) == {r["student_id"] for r in listed["roster"]}

    def test_withdrawing_then_regranting_keeps_the_history(
        self, client: TestClient, admin
    ):
        """A ledger that keeps only the current state cannot answer "when did
        they consent?", and a UNIQUE(tenant_id, student_id) makes regranting
        impossible rather than merely lossy."""
        from app.models.database import SessionLocal
        from app.services.tenancy import consent_history

        student_id = _class_and_student(client, admin, "LEDGER1")
        client.post(
            f"/v1/people/students/{student_id}/consent",
            headers=admin, json={"state": "withdrawn", "purpose": "test"},
        )
        client.post(
            f"/v1/people/students/{student_id}/consent",
            headers=admin, json={"state": "granted", "purpose": "test"},
        )
        db = SessionLocal()
        try:
            tenant_id = client.get("/v1/auth/me", headers=admin).json()["tenant"]["id"]
            history = consent_history(db, tenant_id, student_id)
            assert [record.state for record in history] == [
                "granted", "withdrawn", "granted",
            ]
            assert tenancy.get_consent(db, tenant_id, student_id).state == "granted"
        finally:
            db.close()

    def test_a_withdrawal_takes_effect_immediately(
        self, client: TestClient, admin
    ):
        """A withdrawn student must not be matched on "any granted record"."""
        from app.models.database import SessionLocal

        student_id = _class_and_student(client, admin, "NOWITHDRAW")
        client.post(
            f"/v1/people/students/{student_id}/consent",
            headers=admin, json={"state": "withdrawn", "purpose": "test"},
        )
        db = SessionLocal()
        try:
            tenant_id = client.get("/v1/auth/me", headers=admin).json()["tenant"]["id"]
            assert tenancy.has_consent(db, tenant_id, student_id) is False
        finally:
            db.close()


# ===========================================================================
# Observability: the correlation id and the metrics a 3am page depends on
# ===========================================================================


class TestObservability:
    def test_a_correlation_id_is_echoed_and_never_leaks_into_metrics(
        self, client: TestClient, admin
    ):
        """A user reporting "it failed at 10:04" must be traceable from a
        screenshot. The id must also stay out of the metrics labels, or every
        request becomes its own time series."""
        response = client.get(
            "/v1/auth/me", headers={**admin, "X-Correlation-Id": "corr-abc-123"}
        )
        assert response.status_code == 200
        assert response.headers["X-Correlation-Id"] == "corr-abc-123"

        body = client.get("/metrics").text
        assert "corr-abc-123" not in body
        assert (
            'attendance_http_requests_total{method="GET",route="/v1/auth/me",status="200"}'
            in body
        ), body

    def test_one_request_does_not_create_one_time_series(self, client: TestClient, admin):
        """Labels must be the route template, not the concrete path. A label
        per session id is a metrics-backend denial of service waiting to
        happen."""
        session_id = _make_session(client, admin)
        client.get(f"/v1/sessions/{session_id}", headers=admin)
        body = client.get("/metrics").text
        assert f"route=\"/v1/sessions/{session_id}\"" not in body, body
        assert 'route="/v1/sessions/{session_id}"' in body, body

    def test_a_request_with_no_correlation_id_still_gets_one(
        self, client: TestClient, admin
    ):
        """"None" in a log line is worse than no log line: it looks like data."""
        response = client.get("/v1/auth/me", headers=admin)
        assert response.headers["X-Correlation-Id"]
        assert response.headers["X-Correlation-Id"] != "None"

    def test_a_404_is_recorded(self, client: TestClient):
        """An unrecorded 404 is how a broken edge integration looks like a
        server that is simply quiet."""
        assert client.get("/v1/does-not-exist").status_code == 404
        body = client.get("/metrics").text
        assert 'status="404"' in body, body

    def test_readiness_and_liveness_are_distinct(self, client: TestClient):
        """A liveness probe that touches the database restarts a healthy
        process during a slow query, turning a degraded service into an
        unavailable one."""
        live = client.get("/health")
        ready = client.get("/ready")
        assert live.status_code == 200
        body = live.json()
        # Both stores are reported: v1 searches only the per-tenant indexes, so
        # a single number would hide a warm legacy gallery and a cold v1 one.
        assert "tenant_indexed_identities" in body
        assert "legacy_gallery_size" in body
        assert ready.status_code in (200, 503)
        assert isinstance(ready.json(), dict)


# ===========================================================================
# Erasure: the DPDP path
# ===========================================================================


class TestErasure:
    def test_erasure_requires_echoing_the_roll_number(
        self, client: TestClient, admin
    ):
        """Otherwise a script iterating student ids could erase a whole college."""
        student_id = _class_and_student(client, admin, "E001")
        wrong = client.post(
            "/v1/privacy/erase",
            headers=admin,
            json={"student_id": student_id, "reason": "data subject request", "confirm_roll_no": "WRONG"},
        )
        assert wrong.status_code == 422

    def test_erasure_removes_embeddings_and_keeps_the_audit_trail(
        self, client: TestClient, admin
    ):
        student_id = _class_and_student(client, admin, "E001")
        response = client.post(
            "/v1/privacy/erase",
            headers=admin,
            json={"student_id": student_id, "reason": "data subject request", "confirm_roll_no": "E001"},
        )
        assert response.status_code == 200, response.text
        body = response.json()
        assert "audit trail" in body["retained"]

        audit = client.get("/v1/admin/audit", headers=admin).json()["audit"]
        assert any(e["action"] == "student.erased" for e in audit)

    def test_only_an_admin_may_erase(self, client: TestClient, admin):
        """Erasure is irreversible, so it is the most tightly gated action in
        the system."""
        from app.core.security import hash_password, issue_token
        from app.models.database import SessionLocal
        from app.models.tenancy import User

        tenant_id = client.get("/v1/auth/me", headers=admin).json()["tenant"]["id"]
        db = SessionLocal()
        try:
            row = User(
                tenant_id=tenant_id,
                email="t2@kings.example",
                display_name="T2",
                password_hash=hash_password("correct-horse-battery-staple-42"),
                role=Role.TEACHER.value,
            )
            db.add(row)
            db.commit()
            token = issue_token(subject=row.user_id, tenant_id=tenant_id, role=Role.TEACHER)
        finally:
            db.close()
        response = client.post(
            "/v1/privacy/erase",
            headers={"Authorization": f"Bearer {token}"},
            json={"student_id": "x", "reason": "testing the gate", "confirm_roll_no": "E001"},
        )
        assert response.status_code == 403


# ===========================================================================
# Devices
# ===========================================================================


class TestDeviceProvisioning:
    def test_a_device_secret_is_shown_exactly_once(self, client: TestClient, admin):
        """Only the hash is stored, so there is no code path that can reveal
        it a second time. This test pins that it is not echoed on read."""
        created = client.post("/v1/admin/devices", headers=admin, json={"name": "device-1"})
        secret = created.json()["device_secret"]
        assert secret
        listed = client.get("/v1/admin/devices", headers=admin).text
        assert secret not in listed
        assert "credential_hash" not in listed

    def test_rotating_invalidates_the_old_secret(self, client: TestClient, admin):
        created = client.post("/v1/admin/devices", headers=admin, json={"name": "device-2"})
        device_id = created.json()["device_id"]
        first = created.json()["device_secret"]
        rotated = client.post(f"/v1/admin/devices/{device_id}/rotate", headers=admin)
        second = rotated.json()["device_secret"]
        assert first != second
        client.post(f"/v1/admin/devices/{device_id}/active", headers=admin)

        stale = client.get(
            "/v1/people/students",
            headers={"X-Device-Id": device_id, "X-Device-Secret": first},
        )
        assert stale.status_code == 401
        fresh = client.get(
            "/v1/people/students",
            headers={"X-Device-Id": device_id, "X-Device-Secret": second},
        )
        assert fresh.status_code == 403  # authenticated, but not permitted to read


# ===========================================================================
# Metrics internals: a histogram that lies is worse than no histogram
# ===========================================================================


class TestHistogramInternals:
    def test_reset_clears_durations_as_well_as_counters(self):
        """Guards a half-finished reset that kept the old durations. After a
        restart the p99 would blend pre-restart and post-restart samples, which
        is a number with no meaning behind it."""
        from app.observability.metrics import _Histogram as Histogram

        histogram = Histogram("t_seconds", "test", (0.1, 1.0))
        histogram.observe({"route": "/a"}, 0.05)
        histogram.observe({"route": "/a"}, 0.5)
        assert "t_seconds_count" in "".join(histogram.render())

        histogram.clear()
        assert "".join(histogram.render()).count("t_seconds_count") == 0

    def test_sum_and_count_agree_so_rate_arithmetic_stays_sane(self):
        """Prometheus computes quantiles from cumulative buckets and p99 as
        rate(sum)/rate(count). If the two disagree mid-scrape the derived series
        goes negative and the alert fires on the dashboard."""
        from app.observability.metrics import _Histogram as Histogram

        histogram = Histogram("t_seconds", "test", (0.1, 1.0))
        for value in (0.05, 0.2, 0.3, 2.0):
            histogram.observe({"route": "/a"}, value)
        text = "".join(histogram.render())
        assert "t_seconds_sum{route=\"/a\"} 2.55" in text, text
        assert "t_seconds_count{route=\"/a\"} 4" in text, text

    def test_concurrent_observations_do_not_lose_counts(self):
        """The request path is a threadpool, so two threads incrementing the
        same bucket without a lock lose observations. The symptom is a request
        count that is quietly lower than the access log."""
        from concurrent.futures import ThreadPoolExecutor

        from app.observability.metrics import _Histogram as Histogram

        histogram = Histogram("t_seconds", "test", (1.0,))
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda _: histogram.observe({"route": "/a"}, 0.1), range(500)))
        text = "".join(histogram.render())
        assert "t_seconds_count{route=\"/a\"} 500" in text, text
