"""Authentication, multi-tenant administration, consent, reporting and audit.

This is the operator-facing API. Everything here is tenant-scoped through
:class:`~app.services.tenancy.TenantContext`, which is derived from a verified
credential, never from the request.

Endpoints are grouped as:

* **auth**        sign in, change password, who am I
* **admin**       tenants, users, devices, models
* **people**      students, consent, gallery
* **sessions**    run a session, ingest frames, close out
* **review**      resolve what the system could not decide
* **reports**     export registers, audit trail
* **privacy**     erasure requests (DPDP Act)

Every mutating endpoint writes an audit row **in the same transaction** as the
change. An audit entry in a separate transaction is a log, not an audit trail:
it can disagree with reality.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import logging
import secrets
import uuid
from datetime import UTC, datetime
from typing import Annotated, Any

import numpy as np
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import DbDep, Scope, require, require_upload
from app.core.config import settings
from app.core.domain.timeutil import iso_utc
from app.core.domain.types import FrameContext
from app.core.security import (
    Role,
    hash_password,
    hash_secret,
    issue_token,
    revoke_all_sessions,
    validate_password_strength,
    verify_password,
)
from app.models import tenancy as models
from app.models.tenancy import (
    CONSENT_GRANTED,
    CONSENT_PENDING,
    CONSENT_WITHDRAWN,
    DEFAULT_DEVICE_SCOPES,
    DEVICE_ACTIVE,
    DEVICE_PENDING,
    DEVICE_REVOKED,
    ROLES,
)
from app.services import erasure as erasure_service
from app.services import tenancy
from app.services.ingest import IngestRefused, ingest_frame
from app.services.tenancy import TenantContext

log = logging.getLogger(__name__)
router = APIRouter(prefix="/v1", tags=["operator"])

#: Review-queue status values. The ORM column default is ``"pending"``, so
#: these are named here rather than imported to keep the set in one place.
REVIEW_PENDING = "pending"
REVIEW_RESOLVED = "resolved"
REVIEW_DISMISSED = "dismissed"
REVIEW_VISITOR = "visitor"


# ---------------------------------------------------------------------------
# Request / response models
# ---------------------------------------------------------------------------


class SignIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=256)


class SignUp(BaseModel):
    tenant_slug: str = Field(min_length=3, max_length=64)
    organisation: str = Field(min_length=2, max_length=200)
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=200)
    password: str = Field(min_length=12, max_length=256)
    role: Role = Role.TEACHER


class ChangePassword(BaseModel):
    current_password: str = Field(min_length=1, max_length=256)
    new_password: str = Field(min_length=12, max_length=256)


class StudentIn(BaseModel):
    roll_no: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    email: EmailStr | None = None
    class_id: str | None = None
    seat_label: str | None = Field(default=None, max_length=32)
    consent_state: str = CONSENT_PENDING


class ConsentIn(BaseModel):
    state: str
    purpose: str = Field(default="classroom attendance", max_length=200)
    retention_days: int | None = Field(default=None, ge=1, le=3653)
    evidence_hash: str | None = Field(default=None, max_length=64)


class ReviewDecision(BaseModel):
    action: str = Field(description="confirm | assign | reject | visitor | skip")
    roll_no: str | None = Field(default=None, max_length=64)
    note: str | None = Field(default=None, max_length=1000)


class EraseRequest(BaseModel):
    student_id: str
    reason: str = Field(min_length=3, max_length=500)
    confirm_roll_no: str = Field(description="Must match the student's roll number.")


class CaptureUpload(BaseModel):
    frame_id: str = Field(min_length=8, max_length=64)
    device_timestamp: datetime | None = None
    camera_angle_deg: float | None = None
    zoom: float | None = None
    correlation_id: str | None = Field(default=None, max_length=64)


class RegisterRow(BaseModel):
    #: Stable id, so a consumer can join this row to a student without relying
    #: on the roll number, which a school may renumber between terms.
    student_id: str
    roll_no: str
    name: str
    status: str
    evidence: int
    best_score: float | None
    angles: list[float]
    consent: str
    note: str | None = None


def _consent_of(db: Session, tenant_id: str, student_id: str) -> models.ConsentRecord:
    """The current consent row, or a synthetic pending one.

    Returning a real object means callers never have to branch on ``None``,
    and "no record" is treated the same as an explicit refusal, which is the
    safe reading of an absent answer.
    """
    record = tenancy.get_consent(db, tenant_id, student_id)
    if record is not None:
        return record
    return models.ConsentRecord(
        consent_id="", tenant_id=tenant_id, student_id=student_id,
        state=models.CONSENT_PENDING, purpose="", created_at=datetime.now(UTC),
    )



# ---------------------------------------------------------------------------
# auth
# ---------------------------------------------------------------------------

auth = APIRouter(prefix="/auth", tags=["auth"])


@auth.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: SignUp, db: DbDep) -> dict[str, Any]:
    """Create a tenant and its first account.

    This is the only endpoint that creates a tenant, and it is open, because a
    closed one requires an administrator to exist before anyone can sign up.
    The first account of a brand-new tenant is always an ADMIN; a later signup
    against an existing tenant is refused, so this cannot be used to add
    yourself to someone else's college.
    """
    existing = tenancy.get_tenant_by_slug(db, payload.tenant_slug)
    if existing is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Tenant {payload.tenant_slug!r} already exists. Ask an administrator "
            "for an account instead of signing up again.",
        )
    try:
        validate_password_strength(payload.password)
    except Exception as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc

    tenant = models.Tenant(
        slug=payload.tenant_slug,
        name=payload.organisation,
        region=settings.aws_region if hasattr(settings, "aws_region") else "ap-south-1",
    )
    db.add(tenant)
    db.flush()
    user = models.User(
        tenant_id=tenant.tenant_id,
        email=payload.email.lower(),
        display_name=payload.display_name,
        password_hash=hash_password(payload.password),
        role=Role.ADMIN.value,
    )
    db.add(user)
    db.add(
        models.AuditLog(
            tenant_id=tenant.tenant_id,
            actor_user_id=user.user_id,
            actor_type="user",
            action="tenant.created",
            resource_type="tenant",
            resource_id=tenant.tenant_id,
            detail_json=json.dumps({"slug": tenant.slug, "by": user.email}),
        )
    )
    db.commit()
    return {
        "tenant_id": tenant.tenant_id,
        "user_id": user.user_id,
        "role": Role.ADMIN.value,
        "token": issue_token(
            subject=user.user_id,
            tenant_id=tenant.tenant_id,
            role=Role.ADMIN,
        ),
    }


@auth.post("/signin")
def signin(payload: SignIn, db: DbDep) -> dict[str, Any]:
    """Exchange credentials for a JWT.

    A wrong email and a wrong password give the same error. Distinguishing them
    turns the sign-in form into an account-existence oracle, which is how a
    breach becomes a targeted phishing list.
    """
    user = db.scalar(
        select(models.User).where(func.lower(models.User.email) == payload.email.lower())
    )
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Email or password is incorrect."
        )
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "This account is disabled.")

    user.last_login_at = datetime.now(UTC)
    db.add(
        models.AuditLog(
            tenant_id=user.tenant_id,
            actor_user_id=user.user_id,
            actor_type="user",
            action="auth.signin",
            resource_type="user",
            resource_id=user.user_id,
        )
    )
    db.commit()
    return {
        "token": issue_token(
            subject=user.user_id,
            tenant_id=user.tenant_id,
            role=Role(user.role),
        ),
        "user_id": user.user_id,
        "tenant_id": user.tenant_id,
        "role": user.role,
        "display_name": user.display_name,
    }


@auth.post("/changepassword")
def change_password(
    payload: ChangePassword, db: DbDep, ctx: Scope = Depends(require("user:manage"))
) -> dict[str, Any]:
    """Change the signed-in user's own password.

    Every previously issued token is invalidated. On a compromised account,
    "log out everywhere" that only affects future logins is not a response.
    """
    user = tenancy.get_user(db, ctx.tenant_id, ctx.actor.actor_id)
    if user is None or not verify_password(payload.current_password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Current password is incorrect.")
    try:
        validate_password_strength(payload.new_password)
    except Exception as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc

    user.password_hash = hash_password(payload.new_password)
    revoke_all_sessions(user)
    db.add(
        ctx.audit(
            "auth.password_changed",
            "user",
            user.user_id,
            all_sessions_revoked=True,
        )
    )
    db.commit()
    return {"status": "ok", "detail": "Password changed. Sign in again."}


@auth.get("/me")
def whoami(db: DbDep, ctx: Scope = Depends(require("session:read"))) -> dict[str, Any]:
    """The signed-in identity, its role, and what that role may do.

    The console calls this on load to decide which controls to show. Returning
    the capability map from the server means the UI cannot drift out of sync
    with the enforcement in :data:`app.core.security.CAPABILITIES`.
    """
    from app.core.security import CAPABILITIES

    tenant = tenancy.get_tenant(db, ctx.tenant_id)
    granted = sorted(
        capability
        for capability, needed in CAPABILITIES.items()
        if not ctx.actor.is_device and ctx.actor.role.allows(needed)
    )
    return {
        "actor_id": ctx.actor.actor_id,
        "actor_type": ctx.actor.actor_type.value,
        "display_name": ctx.actor.display_name,
        "role": ctx.actor.role.value,
        "tenant": {"id": ctx.tenant_id, "name": tenant.name if tenant else None,
                   "slug": tenant.slug if tenant else None},
        "scopes": sorted(ctx.actor.scopes),
        "capabilities": granted,
    }


router.include_router(auth)


# ---------------------------------------------------------------------------
# admin: devices, models, audit
# ---------------------------------------------------------------------------

admin = APIRouter(prefix="/admin", tags=["admin"])


class DeviceIn(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    room_id: str | None = None
    #: Requested scopes. Defaults to upload-only. Anything outside the known
    #: set is a 422 rather than a silent drop, because an operator who asked
    #: for "reports:read" on a camera should learn it will never work.
    scopes: list[str] = Field(default_factory=lambda: json.loads(DEFAULT_DEVICE_SCOPES))


@admin.post("/devices", status_code=status.HTTP_201_CREATED)
def create_device(
    payload: DeviceIn, db: DbDep, ctx: Scope = Depends(require("device:manage"))
) -> dict[str, Any]:
    """Provision an edge node and print its secret exactly once.

    The secret is shown here and never again: only its hash is stored, so
    there is no code path that can reveal it later. Losing it is recoverable
    (rotate the device); leaking it is not.
    """
    if payload.room_id and tenancy.get_room(db, ctx.tenant_id, payload.room_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such room in your organisation.")
    unknown = sorted(set(payload.scopes) - models.KNOWN_DEVICE_SCOPES)
    if unknown:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Unknown device scopes: {', '.join(unknown)}. "
            f"Allowed: {', '.join(sorted(models.KNOWN_DEVICE_SCOPES))}.",
        )
    secret = secrets.token_urlsafe(32)
    device = models.Device(
        tenant_id=ctx.tenant_id,
        name=payload.name,
        room_id=payload.room_id,
        credential_hash=hash_secret(secret),
        scopes=json.dumps(sorted(set(payload.scopes))),
        status=DEVICE_PENDING,
    )
    db.add(device)
    db.add(ctx.audit("device.created", "device", device.device_id,
                     name=payload.name, pending=True))
    db.commit()
    return {
        "device_id": device.device_id,
        "device_secret": secret,
        "scopes": device.scopes_list(),
        "status": device.status,
        "warning": "This secret is shown once. Store it on the edge device now.",
    }


@admin.get("/devices")
def list_devices(db: DbDep, ctx: Scope = Depends(require("session:read"))) -> dict[str, Any]:
    rows = tenancy.list_devices(db, ctx.tenant_id)
    return {
        "devices": [
            {
                "device_id": d.device_id,
                "name": d.name,
                "room_id": d.room_id,
                "status": d.status,
                "last_seen_at": iso_utc(d.last_seen_at),
                "agent_version": d.agent_version,
            }
            for d in rows
        ]
    }


@admin.post("/devices/{device_id}/rotate")
def rotate_device(
    device_id: str, db: DbDep, ctx: Scope = Depends(require("device:manage"))
) -> dict[str, Any]:
    """Issue a new secret, invalidating the old one.

    The rotation path is the recovery path for a lost or suspected-leaked
    credential, so it must not require the old secret.
    """
    device = tenancy.get_device(db, ctx.tenant_id, device_id)
    if device is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such device.")
    secret = secrets.token_urlsafe(32)
    device.credential_hash = hash_secret(secret)
    device.status = DEVICE_ACTIVE
    db.add(ctx.audit("device.rotated", "device", device.device_id))
    db.commit()
    return {"device_id": device.device_id, "device_secret": secret, "status": device.status}


@admin.post("/devices/{device_id}/{state}")
def set_device_state(
    device_id: str, state: str, db: DbDep, ctx: Scope = Depends(require("device:manage"))
) -> dict[str, Any]:
    if state not in (DEVICE_PENDING, DEVICE_ACTIVE, DEVICE_REVOKED):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Unknown state {state!r}.")
    device = tenancy.get_device(db, ctx.tenant_id, device_id)
    if device is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such device.")
    device.status = state
    db.add(ctx.audit("device.state_changed", "device", device.device_id, state=state))
    db.commit()
    return {"device_id": device.device_id, "status": device.status}


@admin.get("/models")
def list_models(
    db: DbDep, ctx: Scope = Depends(require("session:read"))
) -> dict[str, Any]:
    rows = db.scalars(
        select(models.ModelVersion)
        .where(models.ModelVersion.tenant_id == ctx.tenant_id)
        .order_by(models.ModelVersion.created_at.desc())
    ).all()
    return {
        "models": [
            {
                "model_version": m.model_version,
                "detector": m.detector_key,
                "embedder": m.embedder_key,
                "license": m.license_name,
                "commercial_use": m.commercial_use,
                "weights_sha256": m.weights_sha256,
                "status": m.status,
                "validation_tar": m.validation_tar,
                "validation_far": m.validation_far,
                "validation_dataset": m.validation_dataset,
                "measured_at": m.measured_at,
                "notes": m.notes,
            }
            for m in rows
        ]
    }


@admin.get("/audit")
def read_audit(
    db: DbDep,
    ctx: Scope = Depends(require("audit:read")),
    limit: int = Query(default=200, ge=1, le=2000),
    action: str | None = None,
) -> dict[str, Any]:
    entries = tenancy.list_audit(db, ctx.tenant_id, limit=limit, action_prefix=action)
    return {
        "audit": [
            {
                "audit_id": e.audit_id,
                "actor_user_id": e.actor_user_id,
                "actor_type": e.actor_type,
                "action": e.action,
                "resource_type": e.resource_type,
                "resource_id": e.resource_id,
                "detail": json.loads(e.detail_json) if e.detail_json else None,
                "occurred_at": e.occurred_at,
                "correlation_id": e.correlation_id,
            }
            for e in entries
        ]
    }


class UserIn(BaseModel):
    email: EmailStr
    display_name: str = Field(min_length=1, max_length=200)
    role: str
    #: Omit to have a strong password generated and shown once. An admin
    #: choosing someone else's password is a bad habit; this makes the
    #: invite-then-reset path the easy one.
    password: str | None = None


@admin.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserIn, db: DbDep, ctx: Scope = Depends(require("user:manage"))
) -> dict[str, Any]:
    """Add a person to your organisation.

    The first signup for a tenant is its admin; everyone after this is created
    here with an explicit role. That is deliberate: role selection belongs to
    the principal's office, not to whoever happens to register first.
    """
    role = payload.role.lower()
    if role not in ROLES:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Unknown role {payload.role!r}. Allowed: {', '.join(sorted(ROLES))}.",
        )
    if tenancy.find_user(db, ctx.tenant_id, str(payload.email)) is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "That email already has an account here."
        )
    generated = False
    password = payload.password
    if password is None:
        password = secrets.token_urlsafe(18)
        generated = True
    validate_password_strength(password)
    user = models.User(
        tenant_id=ctx.tenant_id,
        email=str(payload.email).lower(),
        display_name=payload.display_name,
        role=role,
        password_hash=hash_password(password),
    )
    db.add(user)
    db.add(ctx.audit("user.created", "user", user.user_id, role=role,
                     email=user.email, generated_password=generated))
    db.commit()
    return {
        "user_id": user.user_id,
        "email": user.email,
        "display_name": user.display_name,
        "role": user.role,
        "temporary_password": password if generated else None,
        "warning": (
            "Shown once. Have them change it at first sign-in."
            if generated
            else "You set this password; ask them to change it."
        ),
    }


@admin.get("/users")
def list_users(db: DbDep, ctx: Scope = Depends(require("user:manage"))) -> dict[str, Any]:
    return {
        "users": [
            {
                "user_id": u.user_id,
                "email": u.email,
                "display_name": u.display_name,
                "role": u.role,
                "is_active": u.is_active,
                "last_login_at": iso_utc(u.last_login_at),
            }
            for u in tenancy.list_users(db, ctx.tenant_id)
        ]
    }


@admin.post("/users/{user_id}/role")
def set_user_role(
    user_id: str,
    db: DbDep,
    ctx: Scope = Depends(require("user:manage")),
    role: str = Query(..., max_length=20),
) -> dict[str, Any]:
    """Change someone's role, e.g. promoting a teacher to admin.

    Refuses to remove the last admin: an organisation with no admin cannot
    recover its own access, and support would be the only way back in.
    """
    user = tenancy.get_user(db, ctx.tenant_id, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such user.")
    new_role = role.lower()
    if new_role not in ROLES:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Unknown role {role!r}. Allowed: {', '.join(sorted(ROLES))}.",
        )
    if user.role == Role.ADMIN.value and new_role != Role.ADMIN.value:
        admins = [
            u for u in tenancy.list_users(db, ctx.tenant_id)
            if u.role == Role.ADMIN.value and u.is_active
        ]
        if len(admins) <= 1:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                "This is the last active admin. Promote someone else first.",
            )
    previous = user.role
    user.role = new_role
    # Role is baked into the token, so outstanding tokens must stop working or
    # a demoted admin stays an admin until their token expires.
    user.tokens_valid_after = datetime.now(UTC)
    db.add(ctx.audit("user.role_changed", "user", user_id,
                     previous=previous, role=new_role, tokens_revoked=True))
    db.commit()
    return {"user_id": user_id, "role": new_role, "previous_role": previous}


router.include_router(admin)


# ---------------------------------------------------------------------------
# people: students, consent, gallery
# ---------------------------------------------------------------------------

people = APIRouter(prefix="/people", tags=["people"])


@people.get("/students")
def list_students(
    db: DbDep,
    ctx: Scope = Depends(require("student:read")),
    class_id: str | None = None,
    include_inactive: bool = False,
) -> dict[str, Any]:
    if class_id:
        rows = tenancy.list_roster(db, ctx.tenant_id, class_id)
    else:
        rows = tenancy.list_students(db, ctx.tenant_id, active_only=not include_inactive)
    return {
        "students": [
            {
                "student_id": s.student_id,
                "roll_no": s.roll_no,
                "name": s.name,
                "email": s.email,
                "gallery_exemplars": s.gallery_embedding_count,
                "consent": _consent_of(db, ctx.tenant_id, s.student_id).state,
                "is_active": s.is_active,
                "erased_at": s.erased_at,
            }
            for s in rows
        ]
    }


@people.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentIn,
    db: DbDep,
    ctx: Scope = Depends(require("student:enroll")),
) -> dict[str, Any]:
    """Create a student, optionally enrolling them in a class.

    A student is created with a consent state, not with an assumption of
    consent. Defaulting to ``pending`` means the safe path is the default path.
    """
    if tenancy.find_student_by_roll(db, ctx.tenant_id, payload.roll_no) is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"Roll number {payload.roll_no!r} is already in use."
        )
    if payload.class_id and tenancy.get_class(db, ctx.tenant_id, payload.class_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such class.")

    student = models.Student(
        tenant_id=ctx.tenant_id,
        roll_no=payload.roll_no.strip().upper(),
        name=payload.name,
        email=payload.email,
    )
    db.add(student)
    db.flush()
    _write_consent(db, ctx, student.student_id, payload.consent_state, "classroom attendance",
                   None, None)
    if payload.class_id:
        tenancy.add_class_member(
            db, ctx.tenant_id, payload.class_id, student.student_id,
            seat_label=payload.seat_label,
        )
    db.add(ctx.audit("student.created", "student", student.student_id, roll_no=student.roll_no))
    db.commit()
    return {"student_id": student.student_id, "roll_no": student.roll_no}


def _write_consent(
    db: Session,
    ctx: TenantContext,
    student_id: str,
    state: str,
    purpose: str,
    retention_days: int | None,
    evidence_hash: str | None,
) -> models.ConsentRecord:
    """Record a consent state change, closing any prior record.

    Consent history is append-only: withdrawing does not erase the record that
    consent was once granted, because "was this person ever consented" is a
    question an audit will ask. The current state is the newest record.
    """
    if state not in (CONSENT_GRANTED, CONSENT_PENDING, CONSENT_WITHDRAWN):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, f"Unknown consent state {state!r}.")
    now = datetime.now(UTC)
    record = models.ConsentRecord(
        tenant_id=ctx.tenant_id,
        student_id=student_id,
        state=state,
        purpose=purpose,
        granted_at=now if state == CONSENT_GRANTED else None,
        withdrawn_at=now if state == CONSENT_WITHDRAWN else None,
        retention_days=retention_days,
        evidence_hash=evidence_hash,
    )
    db.add(record)
    return record


@people.post("/students/{student_id}/consent")
def set_consent(
    student_id: str,
    payload: ConsentIn,
    db: DbDep,
    ctx: Scope = Depends(require("consent:write")),
) -> dict[str, Any]:
    student = tenancy.get_student(db, ctx.tenant_id, student_id)
    if student is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such student.")
    record = _write_consent(
        db, ctx, student_id, payload.state, payload.purpose,
        payload.retention_days, payload.evidence_hash,
    )

    # Withdrawing permission means the face template goes with it. Recording the
    # withdrawal and leaving the vector matchable would be processing without
    # consent, and the register would keep producing attendance for someone who
    # asked to be left alone. Same transaction as the record, so a withdrawal
    # cannot half-apply.
    removal = None
    if payload.state == CONSENT_WITHDRAWN:
        removal = erasure_service.remove_gallery_entries(db, ctx.tenant_id, student_id)
        student.gallery_embedding_count = 0

    db.add(ctx.audit(
        "consent.recorded", "student", student_id, state=payload.state,
        **({"gallery_rows_removed": removal.gallery_rows_removed,
            "index_entries_removed": removal.index_entries_removed,
            "object_keys_pending_deletion": removal.pending_object_deletion}
           if removal else {}),
    ))
    db.commit()
    response: dict[str, Any] = {
        "consent_id": record.consent_id, "state": record.state, "created_at": iso_utc(record.created_at),
    }
    if removal is not None:
        response["gallery_removed"] = removal.gallery_rows_removed
        response["index_entries_removed"] = removal.index_entries_removed
        response["pending_object_deletion"] = removal.pending_object_deletion
    return response


@people.get("/consent/pending")
def pending_consent(
    db: DbDep, ctx: Scope = Depends(require("consent:write"))
) -> dict[str, Any]:
    """Students still awaiting a consent decision.

    Surfaced rather than buried, because a class where a third of the roster is
    pending is a class where a third of the register will be silently wrong.

    Resolved from the newest consent row per student, not by asking whether any
    pending row exists. Once history is append-only those are different
    questions: a student whose guardian form was returned as signed still has a
    pending row on file, and a naive join would keep chasing them forever.
    """
    # The newest row per student, using the same ordering as get_consent so
    # the two can never disagree about what someone's current state is.
    # consent_id is a UUID, so max() over it would rank rows alphabetically at
    # random; the window function keeps the created_at ordering explicit.
    ranked = (
        select(
            models.ConsentRecord.student_id,
            models.ConsentRecord.state,
            func.row_number()
            .over(
                partition_by=models.ConsentRecord.student_id,
                order_by=(
                    models.ConsentRecord.created_at.desc(),
                    models.ConsentRecord.consent_id.desc(),
                ),
            )
            .label("rank"),
        )
        .where(models.ConsentRecord.tenant_id == ctx.tenant_id)
        .subquery()
    )
    rows = db.scalars(
        select(models.Student)
        .join(ranked, ranked.c.student_id == models.Student.student_id)
        .where(
            models.Student.tenant_id == ctx.tenant_id,
            models.Student.is_active.is_(True),
            models.Student.erased_at.is_(None),
            ranked.c.rank == 1,
            ranked.c.state == CONSENT_PENDING,
        )
        .order_by(models.Student.roll_no)
    ).all()
    return {
        "pending": [
            {"student_id": s.student_id, "roll_no": s.roll_no, "name": s.name} for s in rows
        ],
        "count": len(rows),
    }


@people.get("/students/{student_id}/gallery")
def student_gallery(
    student_id: str, db: DbDep, ctx: Scope = Depends(require("student:read"))
) -> dict[str, Any]:
    student = tenancy.get_student(db, ctx.tenant_id, student_id)
    if student is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such student.")
    entries = tenancy.list_gallery(db, ctx.tenant_id, roll_no=student.roll_no)
    return {
        "student_id": student_id,
        "roll_no": student.roll_no,
        "exemplars": [
            {
                "gallery_id": e.gallery_id,
                "quality_score": e.quality_score,
                "model_version": e.model_version,
                "added_via": e.added_via,
                "added_at": e.added_at,
            }
            for e in entries
        ],
        "count": len(entries),
        "auto_confirm_minimum": 3,
    }


# ===========================================================================
# Rooms, classes and rosters
#
# These live between the ``admin`` and ``people`` routers being defined and
# their ``include_router`` calls, because FastAPI copies a sub-router's routes
# at include time: a route appended to ``admin`` after line 483 would not
# appear in the app at all.
# ===========================================================================


class RoomIn(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=2, max_length=200)
    #: Geometry is optional, but a camera should not be commissioned before it
    #: is filled in: the scan planner needs it to decide how far to pan.
    width_m: float | None = Field(default=None, gt=0)
    depth_m: float | None = Field(default=None, gt=0)
    camera_height_m: float | None = Field(default=None, gt=0)
    seat_count: int | None = Field(default=None, gt=0)


@admin.post("/rooms", status_code=status.HTTP_201_CREATED)
def create_room(
    payload: RoomIn, db: DbDep, ctx: Scope = Depends(require("class:manage"))
) -> dict[str, Any]:
    """Register a physical classroom."""
    room = models.Room(tenant_id=ctx.tenant_id, **payload.model_dump())
    db.add(room)
    db.add(ctx.audit("room.created", "room", room.room_id, code=room.code))
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"A room with code {payload.code} already exists."
        ) from exc
    return {"room_id": room.room_id, "code": room.code, "name": room.name}


@admin.get("/rooms")
def list_rooms(db: DbDep, ctx: Scope = Depends(require("session:read"))) -> dict[str, Any]:
    return {
        "rooms": [
            {
                "room_id": r.room_id,
                "code": r.code,
                "name": r.name,
                "width_m": r.width_m,
                "depth_m": r.depth_m,
                "camera_height_m": r.camera_height_m,
                "seat_count": r.seat_count,
                "geometry_measured": r.width_m is not None,
            }
            for r in tenancy.list_rooms(db, ctx.tenant_id)
        ]
    }


class ClassIn(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=2, max_length=200)
    room_id: str | None = None


@people.post("/classes", status_code=status.HTTP_201_CREATED)
def create_class(
    payload: ClassIn, db: DbDep, ctx: Scope = Depends(require("class:manage"))
) -> dict[str, Any]:
    """Create a course section, optionally bound to a room."""
    if payload.room_id and tenancy.get_room(db, ctx.tenant_id, payload.room_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such room in your organisation.")
    klass = models.Class(tenant_id=ctx.tenant_id, **payload.model_dump())
    db.add(klass)
    db.add(ctx.audit("class.created", "class", klass.class_id, code=klass.code))
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status.HTTP_409_CONFLICT, f"A class with code {payload.code} already exists."
        ) from exc
    return {
        "class_id": klass.class_id,
        "code": klass.code,
        "name": klass.name,
        "room_id": klass.room_id,
    }


@people.get("/classes")
def list_classes(db: DbDep, ctx: Scope = Depends(require("session:read"))) -> dict[str, Any]:
    out = []
    for klass in tenancy.list_classes(db, ctx.tenant_id):
        roster = tenancy.list_roster(db, ctx.tenant_id, klass.class_id)
        out.append({
            "class_id": klass.class_id,
            "code": klass.code,
            "name": klass.name,
            "room_id": klass.room_id,
            "roster_size": len(roster),
            "gallery_ready": sum(1 for s in roster if s.gallery_embedding_count > 0),
        })
    return {"classes": out}


@people.get("/classes/{class_id}")
def class_detail(
    class_id: str, db: DbDep, ctx: Scope = Depends(require("session:read"))
) -> dict[str, Any]:
    klass = tenancy.get_class(db, ctx.tenant_id, class_id)
    if klass is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such class.")
    roster = tenancy.list_roster(db, ctx.tenant_id, class_id)
    entries = []
    for s in roster:
        consent = tenancy.get_consent(db, ctx.tenant_id, s.student_id)
        entries.append({
            "student_id": s.student_id,
            "roll_no": s.roll_no,
            "name": s.name,
            "consent_state": consent.state if consent else models.CONSENT_PENDING,
            "gallery_embedding_count": s.gallery_embedding_count,
        })
    return {
        "class_id": klass.class_id,
        "code": klass.code,
        "name": klass.name,
        "room_id": klass.room_id,
        "roster": entries,
    }


class MembersIn(BaseModel):
    student_ids: list[str] = Field(min_length=1, max_length=500)


@people.post("/classes/{class_id}/members")
def add_members(
    class_id: str,
    payload: MembersIn,
    db: DbDep,
    ctx: Scope = Depends(require("class:manage")),
) -> dict[str, Any]:
    """Enrol students in a class. Idempotent, so a re-run of an import is safe.

    Unknown student ids are refused rather than skipped: a roster quietly short
    by one student is how a child goes missing from a register.
    """
    if tenancy.get_class(db, ctx.tenant_id, class_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such class.")
    added, unknown = [], []
    for student_id in payload.student_ids:
        if tenancy.get_student(db, ctx.tenant_id, student_id) is None:
            unknown.append(student_id)
            continue
        tenancy.add_class_member(db, ctx.tenant_id, class_id, student_id)
        added.append(student_id)
    if unknown:
        db.rollback()
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"{len(unknown)} student(s) are not in your organisation: {', '.join(unknown[:5])}",
        )
    db.add(ctx.audit("class.members_added", "class", class_id, count=len(added)))
    db.commit()
    return {"class_id": class_id, "added": len(added)}


@people.delete("/classes/{class_id}/members/{student_id}")
def remove_member(
    class_id: str,
    student_id: str,
    db: DbDep,
    ctx: Scope = Depends(require("class:manage")),
) -> dict[str, Any]:
    """Soft-drop a student from a class; their attendance history stays."""
    if not tenancy.drop_class_member(db, ctx.tenant_id, class_id, student_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "That student is not on this roster.")
    db.add(ctx.audit("class.member_removed", "class", class_id, student_id=student_id))
    db.commit()
    return {"class_id": class_id, "student_id": student_id, "dropped": True}


@people.post("/students/{student_id}/gallery", status_code=status.HTTP_201_CREATED)
async def enroll_gallery(
    student_id: str,
    photo: Annotated[UploadFile, File()],
    db: DbDep,
    ctx: Scope = Depends(require("student:enroll")),
) -> dict[str, Any]:
    """Enrol one face photo into the tenant's gallery index.

    This is the write side of the identity path. Without it a tenant's index
    stays permanently empty and every frame becomes an unknown cluster, so a
    deployment that can list students but not enrol them is not a deployment.

    Refuses without granted consent, and refuses a photo where no face passes
    the quality gate: an unusable enrolment is worse than none, because the
    roster screen then shows coverage that is not there.
    """
    student = tenancy.get_student(db, ctx.tenant_id, student_id)
    if student is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such student.")
    if not tenancy.has_consent(db, ctx.tenant_id, student_id):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Consent must be granted before biometric enrolment.",
        )
    if photo.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "Only JPEG, PNG or WebP images are accepted.",
        )
    data = await photo.read()
    if not data or len(data) > settings.max_upload_bytes:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Empty or oversized photo.")

    from app.pipeline.perception import process_frame_bytes
    from app.services.gallery import pack_embedding
    from app.services.tenant_index import tenant_indexes

    result = process_frame_bytes(
        data,
        FrameContext(
            frame_id=f"enroll-{student_id}-{uuid.uuid4().hex[:12]}",
            session_id=0,
            tenant_id=ctx.tenant_id,
            captured_at=datetime.now(UTC),
            correlation_id=ctx.actor.correlation_id,
        ),
    )
    embeddings = [f.embedding for f in result.faces if f.embedding is not None]
    if not embeddings:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "No face passed the quality gate in that photo: "
            + "; ".join(reason for _, reason in result.rejected),
        )

    model = tenancy.active_model_version(db, ctx.tenant_id)
    model_version = model.model_version if model else "unknown"
    added, duplicates = [], 0
    for embedding in embeddings:
        raw = np.asarray(embedding, dtype=np.float32)
        entry = tenancy.add_gallery_entry(
            db,
            ctx.tenant_id,
            student_id,
            student.roll_no,
            pack_embedding(raw),
            hashlib.sha256(np.ascontiguousarray(raw).tobytes()).hexdigest(),
            source_object_key=f"enrollment/{student.roll_no}/{uuid.uuid4().hex}",
            added_via="enrollment",
            model_version=model_version,
        )
        if entry is None:
            duplicates += 1
            continue
        db.flush()
        tenant_indexes.add(db, ctx.tenant_id, entry.gallery_id, student.roll_no, raw)
        added.append(entry.gallery_id)
    student.gallery_embedding_count = len(
        tenancy.list_gallery(db, ctx.tenant_id, roll_no=student.roll_no)
    )
    db.add(ctx.audit("student.enrolled", "student", student_id,
                     added=len(added), duplicates=duplicates, model_version=model_version))
    db.commit()
    return {
        "student_id": student_id,
        "roll_no": student.roll_no,
        "added": len(added),
        "duplicates_skipped": duplicates,
        "gallery_embedding_count": student.gallery_embedding_count,
        "model_version": model_version,
    }


router.include_router(people)


# ---------------------------------------------------------------------------
# sessions
# ---------------------------------------------------------------------------

sessions = APIRouter(prefix="/sessions", tags=["sessions"])


class SessionIn(BaseModel):
    class_id: str
    notes: str | None = Field(default=None, max_length=2000)


@sessions.post("", status_code=status.HTTP_201_CREATED)
def start_session(
    payload: SessionIn, db: DbDep, ctx: Scope = Depends(require("session:close"))
) -> dict[str, Any]:
    klass = tenancy.get_class(db, ctx.tenant_id, payload.class_id)
    if klass is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such class.")
    open_session = db.scalar(
        select(models.ClassSession).where(
            models.ClassSession.tenant_id == ctx.tenant_id,
            models.ClassSession.class_id == payload.class_id,
            models.ClassSession.end_time.is_(None),
        )
    )
    if open_session is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Class {klass.code} already has an open session "
            f"({open_session.session_id}) started at {open_session.start_time.isoformat()}. "
            "Close it before starting another.",
        )
    session = tenancy.create_session(db, ctx.tenant_id, payload.class_id)
    session.notes = payload.notes
    db.add(ctx.audit("session.started", "session", str(session.session_id),
                     class_code=klass.code))
    db.commit()
    return {
        "session_id": session.session_id,
        "class_id": klass.class_id,
        "class_code": klass.code,
        "start_time": iso_utc(session.start_time),
        "roster_size": len(tenancy.list_roster(db, ctx.tenant_id, klass.class_id)),
    }


@sessions.get("/{session_id}")
def session_detail(
    session_id: int, db: DbDep, ctx: Scope = Depends(require("session:read"))
) -> dict[str, Any]:
    session = tenancy.get_session(db, ctx.tenant_id, session_id)
    if session is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such session.")
    klass = tenancy.get_class(db, ctx.tenant_id, session.class_id)
    counts = tenancy.tenant_job_counts(db, ctx.tenant_id)
    return {
        "session_id": session.session_id,
        "class_id": session.class_id,
        "class_code": klass.code if klass else None,
        "start_time": iso_utc(session.start_time),
        "end_time": iso_utc(session.end_time),
        "close_reason": session.close_reason,
        "is_incomplete": session.is_incomplete,
        "present_count": session.present_count,
        "absent_count": session.absent_count,
        "unverified_count": session.unverified_count,
        "notes": session.notes,
        "pending_jobs": counts,
    }


@sessions.post("/{session_id}/frames", status_code=status.HTTP_202_ACCEPTED)
async def upload_frame(
    session_id: int,
    meta: Annotated[str, Form()],
    content: Annotated[UploadFile, File()],
    db: DbDep,
    ctx: Scope = Depends(require_upload()),
) -> dict[str, Any]:
    """Ingest one frame. The production perception and identity path.

    This is the endpoint the edge uploader calls. It refuses closed sessions,
    cross-tenant session ids, and duplicate frame ids -- and the duplicate case
    is a success, not an error, because the edge retries at least once by
    design.
    """
    if content.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            "Only JPEG, PNG or WebP images are accepted.")
    try:
        description = CaptureUpload.model_validate_json(meta)
    except Exception as exc:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                            f"Invalid frame metadata: {exc}") from exc
    data = await content.read()
    if not data or len(data) > settings.max_upload_bytes:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Empty or oversized frame.")

    try:
        outcome = ingest_frame(
            db,
            frame_id=description.frame_id,
            session_id=session_id,
            tenant_id=ctx.tenant_id,
            content=data,
            device_id=ctx.actor.actor_id,
            camera_angle_deg=description.camera_angle_deg,
            zoom=description.zoom,
            device_timestamp=description.device_timestamp,
            correlation_id=description.correlation_id or ctx.actor.correlation_id,
        )
    except IngestRefused as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, f"{exc.code}: {exc.message}") from exc
    return {
        "frame_id": outcome.frame_id,
        "duplicate": outcome.duplicate,
        "faces_seen": outcome.faces_seen,
        "faces_accepted": outcome.faces_accepted,
        "faces_rejected": outcome.faces_rejected,
        "events_created": outcome.events_created,
        "marked_present": outcome.marked_present,
        "notes": outcome.notes,
        "timings_ms": outcome.timings_ms,
    }


router.include_router(sessions)


# ---------------------------------------------------------------------------
# review
# ---------------------------------------------------------------------------

review = APIRouter(prefix="/review", tags=["review"])


@review.get("")
def list_review_queue(
    db: DbDep,
    ctx: Scope = Depends(require("review:read")),
    session_id: int | None = None,
    only_pending: bool = True,
) -> dict[str, Any]:
    statement = select(models.ReviewQueueItem).where(
        models.ReviewQueueItem.tenant_id == ctx.tenant_id
    )
    if session_id is not None:
        statement = statement.where(models.ReviewQueueItem.session_id == session_id)
    if only_pending:
        statement = statement.where(models.ReviewQueueItem.status == REVIEW_PENDING)
    rows = db.scalars(statement.order_by(models.ReviewQueueItem.best_score.desc())).all()
    return {
        "items": [
            {
                "review_id": r.review_id,
                "session_id": r.session_id,
                "cluster_id": r.cluster_id,
                "status": r.status,
                "proposed_roll_no": r.proposed_roll_no,
                "best_score": r.best_score,
                "ask_count": r.ask_count,
                "last_asked_at": r.last_asked_at,
                "resolved_roll_no": r.resolved_roll_no,
                "resolved_at": iso_utc(r.resolved_at),
            }
            for r in rows
        ],
        "count": len(rows),
    }


@review.post("/{review_id}/resolve")
def resolve_review(
    review_id: str,
    payload: ReviewDecision,
    db: DbDep,
    ctx: Scope = Depends(require("review:resolve")),
) -> dict[str, Any]:
    """Record a human decision on an unresolved face.

    Every action is reversible: the row is never deleted, only its status
    changes, and :func:`reopen_review` undoes it. An attendance register that
    cannot be corrected after the fact is not a record, it is a verdict.
    """
    item = db.get(models.ReviewQueueItem, review_id)
    if item is None or item.tenant_id != ctx.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such review item.")

    action = payload.action
    if action in ("confirm", "assign"):
        if not payload.roll_no:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                f"'{action}' requires a roll number.")
        if tenancy.find_student_by_roll(db, ctx.tenant_id, payload.roll_no) is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"No student with roll number {payload.roll_no!r} in your organisation. "
                "Enrol the student first, or use 'visitor' for someone not on the roster.",
            )
        item.status = REVIEW_RESOLVED
        item.resolved_roll_no = payload.roll_no.strip().upper()
    elif action == "reject":
        item.status = REVIEW_DISMISSED
    elif action == "visitor":
        item.status = REVIEW_VISITOR
    elif action == "skip":
        item.status = REVIEW_PENDING
    else:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Unknown action {action!r}. Use confirm, assign, reject, visitor or skip.",
        )

    item.resolved_by_user_id = ctx.actor.actor_id
    item.resolved_at = datetime.now(UTC) if action != "skip" else None
    # `action` is the audit's first positional parameter, so the detail key
    # has to be named something else or the call is a duplicate argument.
    db.add(ctx.audit("review.resolved", "review", review_id, resolution=action,
                     roll_no=payload.roll_no, note=payload.note))
    db.commit()
    return {"review_id": review_id, "status": item.status, "resolved_roll_no": item.resolved_roll_no}


@review.post("/{review_id}/reopen")
def reopen_review(
    review_id: str, db: DbDep, ctx: Scope = Depends(require("review:resolve"))
) -> dict[str, Any]:
    item = db.get(models.ReviewQueueItem, review_id)
    if item is None or item.tenant_id != ctx.tenant_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such review item.")
    item.status = REVIEW_PENDING
    item.resolved_roll_no = None
    item.resolved_by_user_id = None
    item.resolved_at = None
    db.add(ctx.audit("review.reopened", "review", review_id))
    db.commit()
    return {"review_id": review_id, "status": item.status}


router.include_router(review)


# ---------------------------------------------------------------------------
# reports
# ---------------------------------------------------------------------------

reports = APIRouter(prefix="/reports", tags=["reports"])


def _build_register(db: Session, tenant_id: str, session_id: int) -> list[RegisterRow]:
    """Assemble the register for one session.

    Every student on the roster appears exactly once, whatever the evidence:
    a student who was never seen is ABSENT, not missing. A register where rows
    disappear is how a teacher concludes the software is unreliable.
    """
    session = tenancy.get_session(db, tenant_id, session_id)
    if session is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such session.")
    roster = tenancy.list_roster(db, tenant_id, session.class_id)
    events = tenancy.list_events(db, tenant_id, session_id)
    reviews = {
        r.cluster_id: r
        for r in db.scalars(
            select(models.ReviewQueueItem).where(
                models.ReviewQueueItem.tenant_id == tenant_id,
                models.ReviewQueueItem.session_id == session_id,
            )
        ).all()
    }

    per_roll: dict[str, list[models.AttendanceEvent]] = {}
    for event in events:
        if event.roll_no:
            per_roll.setdefault(event.roll_no, []).append(event)

    rows: list[RegisterRow] = []
    for student in roster:
        consent = tenancy.get_consent(db, tenant_id, student.student_id)
        consent_state = consent.state if consent else "none"
        student_events = per_roll.get(student.roll_no, [])

        if consent_state != CONSENT_GRANTED:
            # A student without consent is not "absent". They are excluded:
            # asserting that someone was absent from a class requires
            # recognising them, which is the very processing they declined.
            rows.append(RegisterRow(
                student_id=student.student_id,
                roll_no=student.roll_no, name=student.name,
                status="excluded_no_consent", evidence=0, best_score=None,
                angles=[], consent=consent_state,
                note="No attendance decision is recorded for a student without consent.",
            ))
            continue

        confirmed = [e for e in student_events if e.match_type == "confirmed"]
        resolved = [
            r for r in reviews.values()
            if r.resolved_roll_no == student.roll_no
        ]
        if confirmed or resolved:
            status_text = "present"
        elif student_events:
            status_text = "unverified"
        else:
            status_text = "absent"

        scores = [e.confidence_score for e in student_events if e.confidence_score is not None]
        angles = sorted({e.camera_angle_deg for e in student_events if e.camera_angle_deg is not None})
        rows.append(RegisterRow(
            student_id=student.student_id,
            roll_no=student.roll_no, name=student.name, status=status_text,
            evidence=len(student_events),
            best_score=max(scores) if scores else None,
            angles=angles, consent=consent_state,
        ))
    rows.sort(key=lambda r: r.roll_no)
    return rows


@sessions.post("/{session_id}/close")
def close_session(
    session_id: int,
    db: DbDep,
    ctx: Scope = Depends(require("session:close")),
    reason: str = Query(default="completed", max_length=100),
) -> dict[str, Any]:
    """Close a session and freeze its register.

    Idempotent: closing an already-closed session returns the same result
    rather than erroring, because a retried close from a flaky edge link must
    not leave the operator unsure whether it worked.

    The counts come from the register rather than from a running tally, so
    they cannot drift from what a teacher actually sees in the export.
    """
    session = tenancy.get_session(db, ctx.tenant_id, session_id)
    if session is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such session.")
    if session.end_time is not None:
        return {
            "session_id": session.session_id,
            "end_time": iso_utc(session.end_time),
            "already_closed": True,
            "present_count": session.present_count,
            "absent_count": session.absent_count,
            "unverified_count": session.unverified_count,
        }

    rows = _build_register(db, ctx.tenant_id, session_id)
    tally: dict[str, int] = {}
    for row in rows:
        tally[row.status] = tally.get(row.status, 0) + 1

    # A close with unresolved faces is recorded as incomplete. That is the
    # difference between "40 present, verified" and "40 present, 3 of them the
    # operator had to guess at", and both are true at different times.
    unresolved = db.scalar(
        select(func.count(models.ReviewQueueItem.review_id)).where(
            models.ReviewQueueItem.tenant_id == ctx.tenant_id,
            models.ReviewQueueItem.session_id == session_id,
            models.ReviewQueueItem.status == REVIEW_PENDING,
        )
    ) or 0
    session.end_time = datetime.now(UTC)
    session.close_reason = reason
    session.present_count = tally.get("present", 0)
    session.absent_count = tally.get("absent", 0)
    session.unverified_count = tally.get("unverified", 0) + unresolved
    session.is_incomplete = unresolved > 0 or bool(tally.get("excluded_no_consent"))
    db.add(ctx.audit("session.closed", "session", str(session_id), reason=reason,
                     present=session.present_count, absent=session.absent_count,
                     unverified=session.unverified_count, incomplete=session.is_incomplete))
    db.commit()
    return {
        "session_id": session.session_id,
        "end_time": iso_utc(session.end_time),
        "already_closed": False,
        "present_count": session.present_count,
        "absent_count": session.absent_count,
        "unverified_count": session.unverified_count,
        "is_incomplete": session.is_incomplete,
        "unresolved_reviews": unresolved,
    }


@reports.get("/sessions/{session_id}/register")
def register(
    session_id: int, db: DbDep, ctx: Scope = Depends(require("attendance:read"))
) -> dict[str, Any]:
    rows = _build_register(db, ctx.tenant_id, session_id)
    # _build_register has already raised 404 for an unknown session, so this
    # lookup cannot return None for a request that got this far.
    session = tenancy.get_session(db, ctx.tenant_id, session_id)
    assert session is not None, "register built for a session that does not exist"
    tally: dict[str, int] = {}
    for row in rows:
        tally[row.status] = tally.get(row.status, 0) + 1
    return {
        "session_id": session_id,
        "class_id": session.class_id,
        "start_time": iso_utc(session.start_time),
        "end_time": iso_utc(session.end_time),
        "closed": session.end_time is not None,
        "rows": [row.model_dump() for row in rows],
        "tally": tally,
    }


@reports.get("/sessions/{session_id}/register.csv")
def register_csv(
    session_id: int, db: DbDep, ctx: Scope = Depends(require("report:export"))
) -> StreamingResponse:
    """CSV export for a college's records system.

    Served as a stream rather than built in memory, and the header is fixed and
    explicit, because a spreadsheet import that silently reorders columns is a
    data-corruption bug that surfaces months later in a marks calculation.
    """
    rows = _build_register(db, ctx.tenant_id, session_id)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow([
        "roll_no", "name", "status", "evidence_count", "best_score",
        "camera_angles_deg", "consent_state", "note",
    ])
    for row in rows:
        writer.writerow([
            row.roll_no, row.name, row.status, row.evidence,
            "" if row.best_score is None else f"{row.best_score:.4f}",
            ";".join(f"{a:.1f}" for a in row.angles), row.consent, row.note or "",
        ])
    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="attendance-{session_id}.csv"'},
    )


router.include_router(reports)


# ---------------------------------------------------------------------------
# privacy: DPDP erasure
# ---------------------------------------------------------------------------

privacy = APIRouter(prefix="/privacy", tags=["privacy"])


@privacy.post("/erase")
def erase_student(
    payload: EraseRequest,
    db: DbDep,
    ctx: Scope = Depends(require("student:erase")),
) -> dict[str, Any]:
    """Erase a student's biometric data on request.

    This is the DPDP Act erasure path, so it is deliberately hard to trigger by
    accident: the caller must echo the roll number, which proves a human read
    the record rather than a script iterating student ids.

    What is deleted: face embeddings, gallery rows, attendance event vectors,
    and stored face crops. What is kept: the fact that erasure happened, and
    the audit trail. Keeping the vector "just in case" would make the erasure
    request meaningless, and deleting the audit row would destroy the only
    evidence the request was honoured.
    """
    student = tenancy.get_student(db, ctx.tenant_id, payload.student_id)
    if student is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such student.")
    if student.roll_no != payload.confirm_roll_no:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            f"Roll number does not match. Erasure of {student.roll_no} requires "
            "echoing that roll number exactly.",
        )

    removal = erasure_service.erase_student(db, ctx.tenant_id, student)
    db.add(ctx.audit("student.erased", "student", student.student_id, reason=payload.reason,
                     **removal.as_audit_details()))
    db.commit()
    return removal.as_response(student_id=student.student_id, erased_at=student.erased_at)


router.include_router(privacy)


__all__ = ["router"]
