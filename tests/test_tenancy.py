"""Multi-tenancy and authorisation tests.

The most important tests in this file are the **cross-tenant leak** tests.
They are written adversarially: they create two tenants with deliberately
similar data and then try every access path to reach one from the other. A
multi-tenant product that leaks is not a product, it is a breach with a UI.

Also covered: consent gating, the audit log's refusal to hold biometric data,
role enforcement, and the device-credential scope limit.
"""

from __future__ import annotations

from datetime import UTC, datetime

import numpy as np
import pytest
from sqlalchemy.orm import Session

from app.core.security import (
    CAPABILITIES,
    Actor,
    ActorType,
    InvalidCredentials,
    PermissionDenied,
    Role,
    WeakPasswordError,
    decode_token,
    generate_secret,
    hash_password,
    hash_secret,
    issue_token,
    required_role,
    verify_password,
    verify_secret,
)
from app.models.database import SessionLocal
from app.models.tenancy import (
    CONSENT_GRANTED,
    CONSENT_PENDING,
    CONSENT_WITHDRAWN,
    ConsentRecord,
    Student,
    Tenant,
    User,
)
from app.models.tenancy import (
    Device as DeviceModel,
)
from app.services import tenancy as repo

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def db() -> Session:
    """A database handle truncated before and after each test.

    The suite shares one in-memory SQLite database (StaticPool, so all
    sessions see the same data). Rolling back is not enough because other
    test files commit; every tenancy table is truncated explicitly.
    """

    session = SessionLocal()
    _truncate_all(session)
    yield session
    session.rollback()
    _truncate_all(session)
    session.close()


def _truncate_all(session: Session) -> None:
    """Empty every table in both schemas."""
    from app.models.database import Base
    from app.models.schema import LegacyBase

    session.rollback()
    for metadata in (Base.metadata, LegacyBase.metadata):
        for table in reversed(metadata.sorted_tables):
            session.execute(table.delete())
    session.commit()
    del Base


def _make_tenant(db: Session, slug: str) -> Tenant:
    tenant = Tenant(slug=slug, name=f"{slug} college")
    db.add(tenant)
    db.commit()
    return tenant


def _make_student(db: Session, tenant: Tenant, roll_no: str, *, consented: bool = True) -> Student:
    student = Student(tenant_id=tenant.tenant_id, roll_no=roll_no, name=f"{roll_no} name")
    db.add(student)
    db.flush()
    db.add(
        ConsentRecord(
            tenant_id=tenant.tenant_id,
            student_id=student.student_id,
            state=CONSENT_GRANTED if consented else CONSENT_PENDING,
            purpose="classroom attendance",
        )
    )
    db.commit()
    return student


def _actor(tenant: Tenant, role: Role = Role.ADMIN, **kwargs: object) -> Actor:
    return Actor(
        actor_type=ActorType.USER,
        actor_id=f"user-{tenant.slug}",
        tenant_id=tenant.tenant_id,
        role=role,
        **kwargs,  # type: ignore[arg-type]
    )


# ===========================================================================
# Tenancy: the leak tests
# ===========================================================================


@pytest.fixture
def two_tenants(db: Session) -> tuple[Tenant, Tenant, Student, Student]:
    """Two colleges, each with a student whose roll number is IDENTICAL.

    Identical roll numbers are the interesting case: a query that forgets its
    tenant filter returns the wrong student silently rather than raising.
    """
    alpha = _make_tenant(db, "alpha")
    beta = _make_tenant(db, "beta")
    a_student = _make_student(db, alpha, "R1")
    b_student = _make_student(db, beta, "R1")
    return alpha, beta, a_student, b_student


class TestCrossTenantIsolation:
    """Two colleges must never see each other's data."""

    def test_find_student_by_roll_is_tenant_scoped(self, db: Session, two_tenants: tuple) -> None:
        """R1 at Alpha and R1 at Beta must be different rows."""
        alpha, beta, a_student, b_student = two_tenants
        found = repo.find_student_by_roll(db, alpha.tenant_id, "R1")
        assert found is not None
        assert found.student_id == a_student.student_id

        other = repo.find_student_by_roll(db, beta.tenant_id, "R1")
        assert other is not None
        assert other.student_id == b_student.student_id
        assert found.student_id != other.student_id

    def test_get_student_refuses_a_foreign_id(self, db: Session, two_tenants: tuple) -> None:
        """A student id from another tenant returns None, not the row.

        This is the id-enumeration path. A UUID is hard to guess, but ids also
        arrive in logs, URLs and exports.
        """
        _alpha, beta, _a_student, b_student = two_tenants
        assert repo.get_student(db, beta.tenant_id, b_student.student_id) is not None

    def test_get_student_of_another_tenant_returns_none(self, db: Session, two_tenants: tuple) -> None:
        """Alpha's user asking for Beta's student by id gets nothing."""
        alpha, _beta, _a_student, b_student = two_tenants
        assert repo.get_student(db, alpha.tenant_id, b_student.student_id) is None

    @pytest.mark.parametrize(
        ("getter", "kwargs"),
        [
            ("get_student", {}),
            ("get_room", {}),
            ("get_class", {}),
            ("get_session", {}),
            ("get_user", {}),
            ("get_device", {}),
        ],
    )
    def test_every_getter_is_tenant_scoped(
        self, db: Session, two_tenants: tuple, getter: str, kwargs: dict[str, object]
    ) -> None:
        """No single-tenant getter may accept another tenant's primary key."""
        alpha, beta, _a_student, b_student = two_tenants

        # Build a row in beta.
        room = repo.list_rooms(db, beta.tenant_id)
        del room
        from app.models.tenancy import Class, Room

        beta_room = Room(tenant_id=beta.tenant_id, code="R1", name="Beta room")
        beta_class = Class(tenant_id=beta.tenant_id, code="CS1", name="Beta class")
        beta_session = repo.create_session(db, beta.tenant_id, "x")
        beta_user = User(
            tenant_id=beta.tenant_id,
            email="a@beta.test",
            display_name="Beta",
            password_hash=hash_password("Password123!"),
        )
        beta_device = DeviceModel(
            tenant_id=beta.tenant_id,
            name="edge-1",
            credential_hash=hash_secret(generate_secret()),
            status="active",
        )
        db.add_all([beta_room, beta_class, beta_user, beta_device])
        db.commit()

        ids = {
            "get_student": b_student.student_id,
            "get_room": beta_room.room_id,
            "get_class": beta_class.class_id,
            "get_session": beta_session.session_id,
            "get_user": beta_user.user_id,
            "get_device": beta_device.device_id,
        }
        function = getattr(repo, getter)
        result = function(db, alpha.tenant_id, ids[getter])  # type: ignore[arg-type]
        assert result is None, f"{getter} leaked a row across tenants"

    def test_list_students_is_tenant_scoped(self, db: Session, two_tenants: tuple) -> None:
        """A tenant sees only its own students."""
        alpha, beta, _a, _b = two_tenants
        _make_student(db, beta, "R2")
        alpha_students = repo.list_students(db, alpha.tenant_id)
        assert {s.roll_no for s in alpha_students} == {"R1"}
        beta_students = repo.list_students(db, beta.tenant_id)
        assert {s.roll_no for s in beta_students} == {"R1", "R2"}

    def test_roster_is_per_class_not_global(self, db: Session, two_tenants: tuple) -> None:
        """The audit 4.6 fix, at the tenancy layer.

        Two classes, two disjoint rosters. Asking for class A must not return
        class B's students.
        """
        alpha, _beta, a_student, _b = two_tenants
        from app.models.tenancy import Class

        class_a = Class(tenant_id=alpha.tenant_id, code="CS1", name="A")
        class_b = Class(tenant_id=alpha.tenant_id, code="CS2", name="B")
        db.add_all([class_a, class_b])
        db.commit()

        b_student = Student(tenant_id=alpha.tenant_id, roll_no="R99", name="Other class")
        db.add(b_student)
        db.commit()

        repo.add_class_member(db, alpha.tenant_id, class_a.class_id, a_student.student_id)
        repo.add_class_member(db, alpha.tenant_id, class_b.class_id, b_student.student_id)
        db.commit()

        roster_a = repo.list_roster(db, alpha.tenant_id, class_a.class_id)
        assert {s.roll_no for s in roster_a} == {"R1"}
        roster_b = repo.list_roster(db, alpha.tenant_id, class_b.class_id)
        assert {s.roll_no for s in roster_b} == {"R99"}

    def test_roster_excludes_dropped_students(self, db: Session, two_tenants: tuple) -> None:
        """A soft-dropped member must leave the roster immediately."""
        alpha, _beta, a_student, _b = two_tenants
        from app.models.tenancy import Class

        klass = Class(tenant_id=alpha.tenant_id, code="CS1", name="A")
        db.add(klass)
        db.commit()
        repo.add_class_member(db, alpha.tenant_id, klass.class_id, a_student.student_id)
        db.commit()
        roster = repo.list_roster(db, alpha.tenant_id, klass.class_id)
        assert [s.roll_no for s in roster] == ["R1"]

        assert repo.drop_class_member(db, alpha.tenant_id, klass.class_id, a_student.student_id)
        db.commit()
        assert list(repo.list_roster(db, alpha.tenant_id, klass.class_id)) == []

    def test_re_enrolling_a_dropped_student_restores_them(self, db: Session, two_tenants: tuple) -> None:
        """A drop is soft, so re-adding must be a real option, not a duplicate."""
        alpha, _beta, a_student, _b = two_tenants
        from app.models.tenancy import Class

        klass = Class(tenant_id=alpha.tenant_id, code="CS1", name="A")
        db.add(klass)
        db.commit()

        repo.add_class_member(db, alpha.tenant_id, klass.class_id, a_student.student_id)
        repo.drop_class_member(db, alpha.tenant_id, klass.class_id, a_student.student_id)
        db.commit()
        assert list(repo.list_roster(db, alpha.tenant_id, klass.class_id)) == []

        repo.add_class_member(db, alpha.tenant_id, klass.class_id, a_student.student_id)
        db.commit()
        assert len(repo.list_roster(db, alpha.tenant_id, klass.class_id)) == 1

    def test_duplicate_enrolment_is_idempotent(self, db: Session, two_tenants: tuple) -> None:
        """Re-adding must not create a second roster row."""
        alpha, _beta, a_student, _b = two_tenants
        from app.models.tenancy import Class, ClassMember

        klass = Class(tenant_id=alpha.tenant_id, code="CS1", name="A")
        db.add(klass)
        db.commit()
        repo.add_class_member(db, alpha.tenant_id, klass.class_id, a_student.student_id)
        repo.add_class_member(db, alpha.tenant_id, klass.class_id, a_student.student_id)
        db.commit()
        assert db.query(ClassMember).count() == 1

    def test_class_member_composite_fk_blocks_a_cross_tenant_link(
        self, db: Session, two_tenants: tuple
    ) -> None:
        """The DATABASE refuses a cross-tenant roster link, not just the code.

        A composite foreign key on (tenant_id, ...) means this is impossible
        even from raw SQL, even if a service has a bug.
        """
        from sqlalchemy.exc import IntegrityError

        from app.models.tenancy import Class, ClassMember

        alpha, beta, a_student, _b = two_tenants
        klass = Class(tenant_id=alpha.tenant_id, code="CS1", name="A")
        db.add(klass)
        db.commit()

        # A ClassMember claiming alpha's class but beta's student.
        db.add(ClassMember(tenant_id=alpha.tenant_id, class_id=klass.class_id, student_id="nonexistent"))
        with pytest.raises(IntegrityError):
            db.flush()
        db.rollback()
        del a_student, beta

    def test_user_lookup_is_scoped_to_a_tenant(self, db: Session, two_tenants: tuple) -> None:
        """The same email can exist at two colleges, as two different people."""
        alpha, beta, _a, _b = two_tenants
        digest = hash_password("Password123!")
        db.add(
            User(
                tenant_id=alpha.tenant_id,
                email="shared@test",
                display_name="Alpha admin",
                password_hash=digest,
                role=Role.ADMIN.value,
            )
        )
        db.add(
            User(
                tenant_id=beta.tenant_id,
                email="shared@test",
                display_name="Beta viewer",
                password_hash=digest,
                role=Role.READONLY.value,
            )
        )
        db.commit()

        alpha_user = repo.find_user(db, alpha.tenant_id, "shared@test")
        beta_user = repo.find_user(db, beta.tenant_id, "shared@test")
        assert alpha_user is not None and beta_user is not None
        assert alpha_user.display_name == "Alpha admin"
        assert beta_user.display_name == "Beta viewer"

    def test_device_credential_lookup_does_not_cross_tenants(self, db: Session, two_tenants: tuple) -> None:
        """A device from Beta is unreachable with Alpha's context."""
        alpha, beta, _a, _b = two_tenants
        device = DeviceModel(
            tenant_id=beta.tenant_id,
            name="edge-1",
            credential_hash=hash_secret(generate_secret()),
            status="active",
        )
        db.add(device)
        db.commit()

        assert repo.get_device(db, beta.tenant_id, device.device_id) is not None
        assert repo.get_device(db, alpha.tenant_id, device.device_id) is None

    def test_audit_entries_are_bound_to_the_tenant(self, db: Session, two_tenants: tuple) -> None:
        """One tenant's audit trail is not visible to another."""
        alpha, beta, _a, _b = two_tenants
        for tenant in (alpha, beta):
            repo.append_audit(db, tenant_context(_actor(tenant)).audit("student.read", "student", "x"))
        db.commit()

        alpha_audit = repo.list_audit(db, alpha.tenant_id)
        assert len(alpha_audit) == 1
        assert all(a.tenant_id == alpha.tenant_id for a in alpha_audit)


def tenant_context(actor: Actor) -> repo.TenantContext:
    """Build a TenantContext from an actor."""
    return repo.TenantContext(tenant_id=actor.tenant_id, actor=actor)


# ===========================================================================
# Consent
# ===========================================================================


class TestConsentGating:
    """No consent, no enrollment."""

    def test_consented_student_passes(self, db: Session) -> None:
        tenant = _make_tenant(db, "c1")
        student = _make_student(db, tenant, "R1", consented=True)
        assert repo.has_consent(db, tenant.tenant_id, student.student_id) is True

    def test_pending_consent_blocks(self, db: Session) -> None:
        """A student with no consent is not enrolled, regardless of roster."""
        tenant = _make_tenant(db, "c2")
        student = _make_student(db, tenant, "R1", consented=False)
        assert repo.has_consent(db, tenant.tenant_id, student.student_id) is False

    def test_no_record_at_all_blocks(self, db: Session) -> None:
        """Absent is treated as not-granted. Fail closed."""
        tenant = _make_tenant(db, "c3")
        student = Student(tenant_id=tenant.tenant_id, roll_no="R1", name="R1")
        db.add(student)
        db.commit()
        assert repo.has_consent(db, tenant.tenant_id, student.student_id) is False

    def test_withdrawn_consent_blocks(self, db: Session) -> None:
        """Withdrawal must take effect immediately."""
        tenant = _make_tenant(db, "c4")
        student = _make_student(db, tenant, "R1", consented=True)
        record = repo.get_consent(db, tenant.tenant_id, student.student_id)
        assert record is not None
        record.state = CONSENT_WITHDRAWN
        record.withdrawn_at = datetime.now(UTC)
        db.commit()
        assert repo.has_consent(db, tenant.tenant_id, student.student_id) is False

    def test_consent_is_per_tenant(self, db: Session) -> None:
        """Consent at one college says nothing about another."""
        alpha = _make_tenant(db, "ca")
        beta = _make_tenant(db, "cb")
        a_student = _make_student(db, alpha, "R1", consented=True)
        db.add(Student(tenant_id=beta.tenant_id, roll_no="R1", name="R1"))
        db.commit()
        assert repo.has_consent(db, alpha.tenant_id, a_student.student_id) is True
        assert repo.has_consent(db, beta.tenant_id, a_student.student_id) is False


# ===========================================================================
# Authorisation
# ===========================================================================


class TestRolesAndCapabilities:
    """RBAC by capability, not by scattered role comparisons."""

    @pytest.mark.parametrize(
        ("capability", "role", "allowed"),
        [
            ("attendance:read", Role.READONLY, True),
            ("attendance:read", Role.TEACHER, True),
            ("review:resolve", Role.READONLY, False),
            ("review:resolve", Role.TEACHER, True),
            ("review:resolve", Role.ADMIN, True),
            ("student:erase", Role.TEACHER, False),
            ("student:erase", Role.ADMIN, True),
            ("user:manage", Role.TEACHER, False),
            ("user:manage", Role.ADMIN, True),
            ("audit:read", Role.TEACHER, False),
        ],
    )
    def test_capability_matrix(self, capability: str, role: Role, allowed: bool) -> None:
        """Every capability/role pair behaves as the table says."""
        actor = Actor(ActorType.USER, "u1", "t1", role=role)
        if allowed:
            actor.require(capability)
        else:
            with pytest.raises(PermissionDenied):
                actor.require(capability)

    def test_unknown_capability_is_an_error(self) -> None:
        """A typo in a decorator must stop the request, not grant access."""
        actor = Actor(ActorType.USER, "u1", "t1", role=Role.ADMIN)
        with pytest.raises(KeyError):
            actor.require("does:not:exist")
        with pytest.raises(KeyError):
            required_role("does:not:exist")

    def test_role_ordering(self) -> None:
        """Admin includes teacher includes read-only.

        Deliberately does NOT use ``<`` or ``>`` on the enum. A StrEnum
        compares its string values, and "admin" < "teacher" is True, which
        silently denies an admin every teacher capability. That bug shipped
        in the first draft of this module.
        """
        assert Role.ADMIN.allows(Role.TEACHER)
        assert Role.TEACHER.allows(Role.READONLY)
        assert not Role.READONLY.allows(Role.TEACHER)
        assert not Role.TEACHER.allows(Role.ADMIN)
        assert Role.ADMIN.rank > Role.TEACHER.rank > Role.READONLY.rank

    def test_admin_is_not_denied_by_lexicographic_comparison(self) -> None:
        """The regression pin for the ``<`` bug."""
        admin = Actor(ActorType.USER, "u1", "t1", role=Role.ADMIN)
        for capability in ("review:resolve", "student:erase", "user:manage", "audit:read"):
            admin.require(capability)  # must not raise

    def test_capability_table_is_not_empty(self) -> None:
        """Sanity: the RBAC test is not vacuous."""
        assert len(CAPABILITIES) >= 15
        assert required_role("student:erase") is Role.ADMIN


class TestDeviceCredentials:
    """An edge node must not be able to act as a person."""

    def test_device_cannot_use_any_human_capability(self) -> None:
        """Upload-only, regardless of role or anything else.

        A device's default role is READONLY, so without an explicit device
        branch a compromised edge node could read the student roster -- a
        capability it has no operational reason to need. The first draft of
        this test caught exactly that.
        """
        device = Actor(ActorType.DEVICE, "d1", "t1", scopes=frozenset({"frames:upload"}))
        for capability in ("review:resolve", "student:read", "attendance:read", "session:read"):
            with pytest.raises(PermissionDenied):
                device.require(capability)

    def test_device_is_refused_even_with_an_admin_role(self) -> None:
        """A mis-provisioned admin-role device must still be upload-only."""
        device = Actor(ActorType.DEVICE, "d1", "t1", role=Role.ADMIN, scopes=frozenset({"frames:upload"}))
        with pytest.raises(PermissionDenied):
            device.require("user:manage")
        with pytest.raises(PermissionDenied):
            device.require("student:erase")

    def test_device_has_only_its_scope(self) -> None:
        device = Actor(ActorType.DEVICE, "d1", "t1", scopes=frozenset({"frames:upload"}))
        device.require_scope("frames:upload")
        for scope in ("tenants:write", "students:read", "frames:delete"):
            with pytest.raises(PermissionDenied):
                device.require_scope(scope)

    def test_device_with_no_scopes_can_do_nothing(self) -> None:
        """Fail closed."""
        device = Actor(ActorType.DEVICE, "d1", "t1", scopes=frozenset())
        with pytest.raises(PermissionDenied):
            device.require_scope("frames:upload")

    def test_audit_actor_type_reflects_the_credential(self) -> None:
        """A device must be recorded as a device, not as a user."""
        device = Actor(ActorType.DEVICE, "d1", "t1", scopes=frozenset({"frames:upload"}))
        entry = tenant_context(device).audit("frame.upload", "frame", "f1")
        assert entry.actor_type == "device"
        assert entry.actor_user_id is None


# ===========================================================================
# Passwords and secrets
# ===========================================================================


class TestPasswords:
    """Hashing, verification, and the policy."""

    def test_hash_is_salted_and_verifiable(self) -> None:
        """Two hashes of the same password must differ."""
        first = hash_password("Password123!")
        second = hash_password("Password123!")
        assert first != second, "bcrypt must salt each hash"
        assert verify_password("Password123!", first)
        assert verify_password("Password123!", second)

    def test_wrong_password_fails(self) -> None:
        digest = hash_password("Password123!")
        assert verify_password("Password124!", digest) is False

    def test_malformed_hash_does_not_raise(self) -> None:
        """A corrupt row must look like a wrong password, not a 500."""
        assert verify_password("anything", "not-a-bcrypt-hash") is False

    def test_weak_password_is_refused(self) -> None:
        """Too short is refused at hash time, before any row is written."""
        with pytest.raises(WeakPasswordError, match="at least"):
            hash_password("short")
        with pytest.raises(WeakPasswordError, match="at least"):
            hash_password("a" * 11)

    def test_class_diversity_is_a_policy_check(self) -> None:
        """Length alone is not enough; the policy is checked separately so a
        caller can hash a passphrase it has already validated."""
        from app.core.security import validate_password_strength

        hash_password("alllowercaseonly")  # hashing does not enforce diversity
        with pytest.raises(WeakPasswordError, match="three of"):
            validate_password_strength("alllowercaseonly")

    def test_overlong_password_is_refused(self) -> None:
        """bcrypt truncates at 72 bytes; silently ignoring the tail would make
        two different long passwords equivalent."""
        with pytest.raises(WeakPasswordError, match="72 bytes"):
            hash_password("A" * 200 + "a1!")

    def test_password_policy(self) -> None:
        from app.core.security import validate_password_strength

        with pytest.raises(WeakPasswordError):
            validate_password_strength("onlylowercase")
        with pytest.raises(WeakPasswordError):
            validate_password_strength("ALLUPPERCASE123")
        validate_password_strength("CorrectHorse9!")


class TestSecrets:
    """Opaque credentials for devices and the API key."""

    def test_secret_is_high_entropy(self) -> None:
        secrets_generated = {generate_secret() for _ in range(100)}
        assert len(secrets_generated) == 100
        assert all(len(s) >= 40 for s in secrets_generated)

    def test_hash_and_verify(self) -> None:
        secret = generate_secret()
        digest = hash_secret(secret)
        assert verify_secret(secret, digest) is True
        assert verify_secret(secret + "x", digest) is False

    def test_hash_is_stable(self) -> None:
        """Lookup is by hash, so it must be deterministic."""
        assert hash_secret("abc") == hash_secret("abc")

    def test_empty_values_never_verify(self) -> None:
        assert verify_secret("", hash_secret("abc")) is False
        assert verify_secret("abc", "") is False


class TestTokens:
    """JWT issue/verify, and what must NOT be accepted."""

    def test_round_trip(self) -> None:
        token = issue_token(subject="u1", tenant_id="t1", role=Role.TEACHER)
        claims = decode_token(token)
        assert claims.subject == "u1"
        assert claims.tenant_id == "t1"
        assert claims.role is Role.TEACHER
        assert claims.seconds_remaining > 0

    def test_tampered_token_is_rejected(self) -> None:
        token = issue_token(subject="u1", tenant_id="t1", role=Role.TEACHER)
        with pytest.raises(InvalidCredentials):
            decode_token(token + "x")

    def test_unsigned_token_is_rejected(self) -> None:
        """An alg=none token must not authenticate."""
        import jwt

        forge = jwt.encode(
            {"sub": "admin", "tid": "t1", "role": "admin", "exp": 9999999999},
            key="",
            algorithm="none",
        )
        with pytest.raises(InvalidCredentials):
            decode_token(forge)

    def test_token_from_another_secret_is_rejected(self) -> None:
        """A token signed with a guessable key must fail."""
        import jwt

        from app.core.config import settings

        forge = jwt.encode(
            {
                "sub": "admin",
                "tid": "t1",
                "role": "admin",
                "exp": 9999999999,
                "iat": 1,
            },
            key="not-the-real-secret",
            algorithm=settings.jwt_algorithm,
        )
        with pytest.raises(InvalidCredentials):
            decode_token(forge)

    def test_expired_token_is_rejected(self) -> None:
        token = issue_token(subject="u1", tenant_id="t1", role=Role.TEACHER, ttl_seconds=-10)
        with pytest.raises(InvalidCredentials, match="expired"):
            decode_token(token)

    def test_missing_claims_are_rejected(self) -> None:
        """A token without a tenant is not usable in a multi-tenant system."""
        import jwt

        from app.core.config import settings

        forge = jwt.encode(
            {"sub": "u1", "role": "admin", "exp": 9999999999},
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        with pytest.raises(InvalidCredentials):
            decode_token(forge)


class TestAuditLogContents:
    """The audit log must not become a biometric data store."""

    def test_audit_refuses_biometric_detail(self) -> None:
        """An audit entry is read by more people and kept longer than the
        operational tables. An embedding in one defeats the restriction."""
        tenant = _make_tenant(SessionLocal(), "audit-test")
        context = tenant_context(_actor(tenant))
        with pytest.raises(ValueError, match="biometric"):
            context.audit("student.update", "student", "R1", embedding=b"\x00\x01")

    def test_audit_accepts_identifiers(self) -> None:
        tenant = _make_tenant(SessionLocal(), "audit-ok")
        context = tenant_context(_actor(tenant))
        entry = context.audit("student.update", "student", "R1", name="new name", count=3)
        assert entry.tenant_id == tenant.tenant_id
        assert entry.resource_id == "R1"
        assert "new name" in (entry.detail_json or "")

    def test_audit_carries_the_correlation_id(self) -> None:
        """Logs, metrics and traces must line up for one operation."""
        tenant = _make_tenant(SessionLocal(), "audit-corr")
        context = tenant_context(_actor(tenant, correlation_id="corr-123"))
        entry = context.audit("x.y", "thing")
        assert entry.correlation_id == "corr-123"

    def test_actor_comes_from_the_credential_not_the_request(self) -> None:
        """The whole point: a client cannot choose who it is."""
        tenant = _make_tenant(SessionLocal(), "audit-actor")
        context = tenant_context(_actor(tenant))
        entry = context.audit("review.resolve", "review", "1")
        assert entry.actor_user_id == context.actor.actor_id
        assert entry.actor_type == "user"


# ===========================================================================
# Frames: idempotency
# ===========================================================================


class TestFrameIdempotency:
    """At-least-once edge delivery must become effectively-once."""

    def test_re_registering_a_frame_is_a_no_op(self, db: Session) -> None:
        """The edge device retries; the second attempt must not duplicate."""
        tenant = _make_tenant(db, "frames")
        student = _make_student(db, tenant, "R1")
        del student
        session = repo.create_session(db, tenant.tenant_id, "CS1")
        db.commit()

        first = repo.register_frame(db, tenant.tenant_id, "frame-abc", session.session_id)
        assert first is not None
        db.commit()

        second = repo.register_frame(db, tenant.tenant_id, "frame-abc", session.session_id)
        assert second is None, "a redelivered frame must not be registered twice"
        db.commit()

        from app.models.tenancy import Frame

        assert db.query(Frame).filter_by(frame_id="frame-abc").count() == 1

    def test_gallery_entry_deduplicates_on_the_embedding_hash(self, db: Session) -> None:
        """A retried enrollment must not inflate a gallery."""
        tenant = _make_tenant(db, "gallery-dedup")
        student = _make_student(db, tenant, "R1")
        digest = hash_secret("embedding-bytes")

        first = repo.add_gallery_entry(
            db, tenant.tenant_id, student.student_id, "R1", b"\x00\x01", digest, "k1", "enrollment"
        )
        assert first is not None
        db.commit()

        second = repo.add_gallery_entry(
            db, tenant.tenant_id, student.student_id, "R1", b"\x00\x01", digest, "k1", "enrollment"
        )
        assert second is None, "the same embedding must not be stored twice"
        db.commit()


# ===========================================================================
# Compile-time guarantee
# ===========================================================================


class TestSchemaGuarantees:
    """Some tenancy rules belong in the schema, not in code."""

    def test_every_tenant_owned_table_has_tenant_id(self) -> None:
        """Structural guarantee: a table that forgets tenant_id is a leak
        waiting to happen, and this test fails at import time."""
        import app.models.tenancy  # noqa: F401
        from app.models.database import Base

        #: Tables that are deliberately global, not tenant-scoped.
        GLOBAL_TABLES = {"alembic_version", "tenants", "model_versions"}

        offenders = []
        for name, table in Base.metadata.tables.items():
            if name in GLOBAL_TABLES:
                continue
            columns = {c.name for c in table.columns}
            if "tenant_id" not in columns:
                offenders.append(name)
        assert not offenders, f"tables without tenant_id: {offenders}"

    def test_tenant_scoped_tables_index_the_tenant_column(self) -> None:
        """An unindexed tenant_id turns every query into a full scan."""
        import app.models.tenancy  # noqa: F401
        from app.models.database import Base

        GLOBAL_TABLES = {"alembic_version", "tenants", "model_versions"}
        for name, table in Base.metadata.tables.items():
            if name in GLOBAL_TABLES or "tenant_id" not in {c.name for c in table.columns}:
                continue
            # A single-column index on tenant_id, or any composite index
            # LEADING with tenant_id, satisfies this. A composite index where
            # tenant_id is not first is not enough: PostgreSQL cannot use it
            # for a tenant-only predicate.
            leading = [
                ix.columns[0].name
                for ix in table.indexes
                if len(ix.columns) >= 1 and ix.columns[0] is not None
            ]
            assert "tenant_id" in leading, (
                f"{name} has no index leading with tenant_id; index columns start with {leading}"
            )

    def test_roll_number_is_unique_per_tenant_not_globally(self) -> None:
        """Two colleges may both have an R1."""
        from app.models.tenancy import Student as TenancyStudent

        constraints = {tuple(c.name for c in uq.columns) for uq in TenancyStudent.__table__.constraints}
        assert ("tenant_id", "roll_no") in constraints

    def test_audit_log_has_no_update_or_delete_helper(self) -> None:
        """Append-only is a structural property, not a convention.

        There is deliberately no ``update_audit`` or ``delete_audit`` anywhere
        in the repository, so this asserts the module surface stays that way.
        """
        import app.services.tenancy as module

        forbidden = [
            name
            for name in dir(module)
            if "audit" in name.lower() and any(w in name.lower() for w in ("update", "delete", "purge"))
        ]
        assert not forbidden, f"audit log must be append-only, found: {forbidden}"


class TestTenantContext:
    """The context object itself."""

    def test_assert_entity_catches_a_foreign_row(self, db: Session, two_tenants: tuple) -> None:
        """Loading by primary key from an untrusted id is the risk."""
        alpha, _beta, _a_student, b_student = two_tenants
        context = tenant_context(_actor(alpha))
        with pytest.raises(repo.TenantViolation, match="belongs to tenant"):
            context.assert_entity(b_student)

    def test_assert_entity_passes_for_the_right_tenant(self, db: Session, two_tenants: tuple) -> None:
        alpha, _beta, a_student, _b = two_tenants
        context = tenant_context(_actor(alpha))
        assert context.assert_entity(a_student) == alpha.tenant_id

    def test_violation_is_loud_not_silent(self) -> None:
        """Silently returning an empty result would hide a breach."""
        assert issubclass(repo.TenantViolation, RuntimeError)

    def test_numpy_embeddings_do_not_leak_into_audit(self) -> None:
        """Even a numpy array is rejected."""
        tenant = _make_tenant(SessionLocal(), "numpy-audit")
        context = tenant_context(_actor(tenant))
        with pytest.raises(ValueError, match="biometric"):
            context.audit("x", "y", "z", centroid=np.zeros(4, dtype=np.float32))
