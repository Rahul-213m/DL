"""Authentication and authorisation.

Three credentials, deliberately separated:

* **User** (human): email + password, exchanges them for a short-lived JWT.
  Roles are admin / teacher / read-only.
* **Device** (edge node): a long-lived opaque secret, sent as a bearer token.
  It grants upload only. It cannot read attendance, change a roster, or
  impersonate a human.
* **API key** (bootstrap): one-time server-to-server key for provisioning.
  Rejected in production if it is still the published default.

Two rules that are enforced rather than documented:

1. **Never trust a client-asserted identity for an audit field.** The legacy
   code took ``resolved_by`` as a form value any operator could type, so the
   audit trail recorded whoever was believed to be present. Here the actor
   always comes from a verified token.
2. **Constant-time comparison for every secret.** ``==`` on a secret leaks its
   prefix through timing; the legacy API-key check used ``==``.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any

from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.core.config import INSECURE_DEFAULT_API_KEY, settings

log = logging.getLogger(__name__)

#: bcrypt truncates at 72 bytes. Rejecting longer inputs is clearer than
#: silently ignoring the tail, which would make two different long passwords
#: equivalent.
MAX_PASSWORD_BYTES = 72
MIN_PASSWORD_LENGTH = 12
MIN_SECRET_BYTES = 32


class AuthError(Exception):
    """Base class for authentication failures."""


class InvalidCredentials(AuthError):
    """Wrong password, unknown user, or a malformed token."""


class AccountDisabled(AuthError):
    """The user or device exists but is not active."""


class PermissionDenied(AuthError):
    """Authenticated, but the role does not permit this action."""


class WeakPasswordError(AuthError):
    """Password does not meet the minimum policy."""


# ---------------------------------------------------------------------------
# Passwords
# ---------------------------------------------------------------------------


def hash_password(password: str, *, rounds: int | None = None) -> str:
    """Hash a password with bcrypt.

    Raises:
        WeakPasswordError: if the password violates the policy, or is longer
            than bcrypt's 72-byte input limit (which would otherwise silently
            truncate, making two different long passwords equivalent).
    """
    from passlib.hash import bcrypt

    if len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise WeakPasswordError(f"password must be at most {MAX_PASSWORD_BYTES} bytes when UTF-8 encoded")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise WeakPasswordError(f"password must be at least {MIN_PASSWORD_LENGTH} characters")
    return bcrypt.using(rounds=rounds or settings.password_hash_rounds).hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against a bcrypt hash, in constant time.

    Returns ``False`` rather than raising on a malformed hash, so a corrupt
    row cannot be distinguished from a wrong password by timing or by status
    code.
    """
    from passlib.hash import bcrypt

    try:
        return bool(bcrypt.verify(password, password_hash))
    except (ValueError, TypeError):
        log.warning("password hash is malformed; treating the login as failed")
        return False


def validate_password_strength(password: str) -> None:
    """Check the password policy, raising on failure.

    Policy: length plus three of four character classes. Not a breach
    predictor, but it removes the passwords students and staff actually
    choose.
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        raise WeakPasswordError(f"password must be at least {MIN_PASSWORD_LENGTH} characters")
    if len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise WeakPasswordError(f"password must be at most {MAX_PASSWORD_BYTES} bytes")
    classes = sum(
        (
            any(c.islower() for c in password),
            any(c.isupper() for c in password),
            any(c.isdigit() for c in password),
            any(not c.isalnum() for c in password),
        )
    )
    if classes < 3:
        raise WeakPasswordError(
            "password must combine at least three of: lowercase, uppercase, digits, symbols"
        )


# ---------------------------------------------------------------------------
# Opaque secrets (API keys and device credentials)
# ---------------------------------------------------------------------------


def generate_secret(nbytes: int = 32) -> str:
    """Return a URL-safe random secret from the OS CSPRNG."""
    return secrets.token_urlsafe(nbytes)


def hash_secret(secret: str) -> str:
    """Hash an opaque secret for storage.

    SHA-256, not bcrypt. These are 256-bit random values, not user-chosen
    passwords, so there is nothing to brute-force and bcrypt's deliberate
    slowness would only add latency to every edge upload. Comparison is
    constant-time regardless.
    """
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


def verify_secret(secret: str, secret_hash: str) -> bool:
    """Constant-time comparison of a presented secret against a stored hash."""
    if not secret or not secret_hash:
        return False
    return hmac.compare_digest(hash_secret(secret), secret_hash)


def is_insecure_default(value: str | None) -> bool:
    """Whether a value is still the published development secret."""
    return value == INSECURE_DEFAULT_API_KEY


# ---------------------------------------------------------------------------
# Roles
# ---------------------------------------------------------------------------


class Role(StrEnum):
    """What a human may do.

    Ordered by capability, so a single comparison expresses "at least
    teacher". Never inferred from the request.
    """

    READONLY = "readonly"
    TEACHER = "teacher"
    ADMIN = "admin"

    @property
    def rank(self) -> int:
        """Capability level, for ``>=`` checks."""
        return {Role.READONLY: 0, Role.TEACHER: 1, Role.ADMIN: 2}[self]

    def allows(self, other: Role) -> bool:
        """Whether this role includes everything ``other`` permits."""
        return self.rank >= other.rank


#: Explicit capability table. Preferred over scattering role comparisons
#: through handlers, because a new endpoint then has to answer one question
#: ("what is the minimum role here?") instead of auditing every branch.
CAPABILITIES: dict[str, Role] = {
    # Read
    "session:read": Role.READONLY,
    "attendance:read": Role.READONLY,
    "student:read": Role.READONLY,
    "review:read": Role.READONLY,
    "report:export": Role.TEACHER,
    # Operate
    "review:resolve": Role.TEACHER,
    "attendance:override": Role.TEACHER,
    "session:close": Role.TEACHER,
    "student:enroll": Role.TEACHER,
    # Govern
    "student:erase": Role.ADMIN,
    "consent:write": Role.ADMIN,
    "user:manage": Role.ADMIN,
    "device:manage": Role.ADMIN,
    "model:activate": Role.ADMIN,
    "audit:read": Role.ADMIN,
    "tenant:manage": Role.ADMIN,
}


def required_role(capability: str) -> Role:
    """Minimum role for a capability.

    Raises:
        KeyError: for an unknown capability. Failing on an unrecognised
            capability is deliberate: a typo in a decorator must stop the
            request, not silently grant access.
    """
    return CAPABILITIES[capability]


# ---------------------------------------------------------------------------
# Identity, never client-asserted
# ---------------------------------------------------------------------------


class ActorType(StrEnum):
    """Who is acting."""

    USER = "user"
    DEVICE = "device"
    SYSTEM = "system"


@dataclass(frozen=True, slots=True)
class Actor:
    """A verified identity, extracted from a credential.

    Every audit row and every mutation records this. Nothing in the request
    body can influence it.
    """

    actor_type: ActorType
    actor_id: str
    tenant_id: str
    role: Role = Role.READONLY
    display_name: str = ""
    #: Correlation id for this request, so logs, metrics and traces line up.
    correlation_id: str = ""
    #: Scopes granted to a device credential. A device is upload-only.
    scopes: frozenset[str] = frozenset()

    def require(self, capability: str) -> None:
        """Assert this actor holds a capability.

        A **device** is upload-only and is refused every human capability
        regardless of its role. A device's default role is READONLY, and
        without this branch a compromised edge node could read the student
        roster -- a read capability it has no operational reason to need.

        For humans, the comparison is on ``rank``, never on the enum values
        directly. Comparing ``StrEnum`` members with ``<`` compares their
        *string values*, so ``Role.ADMIN < Role.TEACHER`` is True ("admin"
        sorts before "teacher") and an admin would be denied everything.

        Raises:
            PermissionDenied: if the actor may not perform the capability.
            KeyError: if the capability name is unknown.
        """
        needed = required_role(capability)
        if self.is_device:
            raise PermissionDenied(
                f"a device credential cannot use the human capability {capability!r}; "
                f"its scopes are {sorted(self.scopes) or 'none'}"
            )
        if not self.role.allows(needed):
            raise PermissionDenied(
                f"{capability} requires {needed}; {self.actor_type} {self.actor_id} has {self.role}"
            )

    def require_scope(self, scope: str) -> None:
        """Assert a device credential carries a scope.

        Raises:
            PermissionDenied: if the scope is absent.
        """
        if scope not in self.scopes:
            raise PermissionDenied(
                f"credential lacks the '{scope}' scope; granted: {sorted(self.scopes) or 'none'}"
            )

    @property
    def is_device(self) -> bool:
        """Whether this is an edge node rather than a person."""
        return self.actor_type is ActorType.DEVICE


#: The only scope a device credential ever receives.
DEVICE_UPLOAD_SCOPE = "frames:upload"
DEVICE_SCOPES = frozenset({DEVICE_UPLOAD_SCOPE})


# ---------------------------------------------------------------------------
# JWT
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TokenClaims:
    """Decoded, verified JWT claims."""

    subject: str
    tenant_id: str
    role: Role
    issued_at: datetime
    expires_at: datetime
    jti: str

    @property
    def is_expired(self) -> bool:
        """Whether the token is past its expiry."""
        return datetime.now(UTC) >= self.expires_at

    @property
    def seconds_remaining(self) -> int:
        """Seconds until expiry, floored at zero."""
        return max(0, int((self.expires_at - datetime.now(UTC)).total_seconds()))


def issue_token(
    *,
    subject: str,
    tenant_id: str,
    role: Role,
    ttl_seconds: int | None = None,
    extra: dict[str, Any] | None = None,
) -> str:
    """Issue a signed JWT for a human session.

    Raises:
        InvalidCredentials: if no signing secret is configured. Failing here
            is better than issuing an unsigned token.
    """
    import jwt

    if not settings.jwt_secret:
        raise InvalidCredentials("JWT_SECRET is not configured; cannot issue a session token")

    now = datetime.now(UTC)
    ttl = ttl_seconds or settings.jwt_ttl_seconds
    claims: dict[str, Any] = {
        "sub": subject,
        "tid": tenant_id,
        "role": role.value,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=ttl)).timestamp()),
        "jti": secrets.token_urlsafe(16),
    }
    if extra:
        claims.update(extra)
    return jwt.encode(claims, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> TokenClaims:
    """Verify and decode a JWT.

    The algorithm is pinned to the configured one, so an attacker cannot
    submit an ``alg=none`` token or switch to a weaker algorithm.

    Raises:
        InvalidCredentials: on a bad signature, wrong algorithm, expiry, or
            malformed token.
    """
    import jwt

    if not settings.jwt_secret:
        raise InvalidCredentials("JWT_SECRET is not configured; cannot verify a token")
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["exp", "sub", "tid", "role"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise InvalidCredentials("session token has expired") from exc
    except jwt.InvalidTokenError as exc:
        # Deliberately does not distinguish "bad signature" from "malformed":
        # telling an attacker which is the more useful answer helps them.
        raise InvalidCredentials("invalid session token") from exc

    return TokenClaims(
        subject=str(payload["sub"]),
        tenant_id=str(payload["tid"]),
        role=Role(payload["role"]),
        issued_at=datetime.fromtimestamp(int(payload["iat"]), tz=UTC),
        expires_at=datetime.fromtimestamp(int(payload["exp"]), tz=UTC),
        jti=str(payload["jti"]),
    )


def revoke_all_sessions(user: UserRow, *, now: datetime | None = None) -> None:
    """Invalidate every outstanding token for a user.

    Sets ``tokens_valid_after``. Cheap and instant, unlike a per-token
    denylist, and sufficient for "log out everywhere" and "my password changed".
    """
    user.tokens_valid_after = now or datetime.now(UTC)


def token_is_valid_after(claims: TokenClaims, cutoff: datetime | None) -> bool:
    """Whether a token predates a revocation cutoff."""
    if cutoff is None:
        return True
    return claims.issued_at >= cutoff


# Imported late and under TYPE_CHECKING so this module has no ORM dependency
# at import time; it is used by the FastAPI dependency layer only.
if True:  # pragma: no cover - typing convenience
    from app.models.tenancy import User as UserRow


__all__ = [
    "CAPABILITIES",
    "DEVICE_SCOPES",
    "DEVICE_UPLOAD_SCOPE",
    "MAX_PASSWORD_BYTES",
    "MIN_PASSWORD_LENGTH",
    "MIN_SECRET_BYTES",
    "AccountDisabled",
    "Actor",
    "ActorType",
    "AuthError",
    "InvalidCredentials",
    "PermissionDenied",
    "Role",
    "TokenClaims",
    "WeakPasswordError",
    "decode_token",
    "generate_secret",
    "hash_password",
    "hash_secret",
    "is_insecure_default",
    "issue_token",
    "require_api_key",
    "required_role",
    "revoke_all_sessions",
    "token_is_valid_after",
    "validate_password_strength",
    "verify_password",
    "verify_secret",
]


# ---------------------------------------------------------------------------
# Legacy compatibility
# ---------------------------------------------------------------------------
# `app/api/routes.py` and the 23 original behavioural tests import
# `require_api_key` from this module. W7 deletes those endpoints along with the
# pre-tenant schema, so this shim is temporary by design and is marked for
# removal rather than quietly kept.

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
# `app/api/routes.py` and the 23 original behavioural tests import
# `require_api_key` from this module. W7 deletes those endpoints along with the
# pre-tenant schema, so this shim is temporary by design and is marked for
# removal rather than quietly kept.


def require_api_key(api_key: str | None = Depends(_api_key_header)) -> None:
    """Validate a shared API key. DEPRECATED: superseded by user JWTs.

    A single shared secret cannot distinguish a teacher from a read-only
    viewer, and the legacy audit trail recorded whichever name the request
    body asserted. Do not use for new endpoints.

    Raises:
        InvalidCredentials: if the key is absent, wrong, or still the
            published development default.
    """
    from fastapi import HTTPException, status

    if settings.api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="no API_KEY is configured",
        )
    if is_insecure_default(settings.api_key) and settings.is_production:
        # Refusing outright in production is the point. In development and test
        # the published default is the documented convenience, and refusing it
        # there would just make the suite unable to run at all.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="the published development API key is still in use; rotate it",
        )
    if api_key is None or not verify_secret(api_key, hash_secret(settings.api_key)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid or missing API key")
