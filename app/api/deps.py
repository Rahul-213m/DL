"""Authentication and tenant resolution for every multi-tenant endpoint.

THE ONE RULE
------------
``tenant_id`` is never read from a request body, a query parameter, or a
header. It is derived from a *verified credential*. A handler that wants to know
whose data it is touching asks for :class:`TenantContext` and gets the answer
from the token, the account, or the device record.

This is the difference between multi-tenant software and a data breach with an
API. If a handler can be made to trust a client-supplied tenant id by adding one
parameter, the isolation is decorative.

THREE WAYS IN
-------------
1. **User JWT** — a person signed in with a password. Carries a role; every
   capability is checked against :data:`app.core.security.CAPABILITIES`.
2. **Device credential** — an edge node. Upload-only. It cannot read the roster
   even if its role were tampered with, because :meth:`Actor.require` refuses
   every human capability for a device before the role is even consulted.
3. **Bootstrap API key** — single-tenant installations and the edge bring-up
   window, before a device credential has been provisioned. Refused outright in
   production unless explicitly enabled, because an API key that can reach every
   tenant is not multi-tenant.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterator
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.core.security import (
    DEVICE_UPLOAD_SCOPE,
    Actor,
    ActorType,
    InvalidCredentials,
    PermissionDenied,
    Role,
    decode_token,
)
from app.models.database import SessionLocal
from app.models.tenancy import DEVICE_ACTIVE
from app.services import tenancy
from app.services.tenancy import TenantContext, TenantViolation

log = logging.getLogger(__name__)


def get_db() -> Iterator[Session]:
    """A database handle whose lifetime is the request.

    Deliberately NOT committed here. Each handler commits the transaction that
    contains both its change and its audit row, so an audit entry can never
    outlive the change it describes, or vice versa.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _bearer(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Missing Authorization header. Use 'Authorization: Bearer <token>'.",
        )
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Malformed Authorization header. Expected 'Authorization: Bearer <token>'.",
        )
    return token.strip()


def _device_secret(
    x_device_id: str | None, x_device_secret: str | None
) -> tuple[str, str]:
    if not x_device_id or not x_device_secret:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Device credentials require both X-Device-Id and X-Device-Secret.",
        )
    return x_device_id, x_device_secret


def _bootstrap_api_key(api_key: str | None) -> Actor:
    """Authenticate a single-tenant bootstrap key.

    This is the escape hatch that lets a fresh install work before anybody has
    created an account. It is scoped to ONE tenant -- the one named by
    ``BOOTSTRAP_TENANT_SLUG`` -- precisely so that a leaked key does not become
    a key to every tenant's data.

    Raises:
        HTTPException: in production when bootstrap is not explicitly enabled.
    """
    if not settings.allow_bootstrap_api_key:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "The bootstrap API key is disabled. Create a user account and sign in "
            "with a JWT, or set ALLOW_BOOTSTRAP_API_KEY=true for single-tenant "
            "bring-up. It is refused by default because a key that reaches every "
            "tenant is not multi-tenant.",
        )
    if security.is_insecure_default(api_key):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "The bootstrap API key is a known development default. Generate one "
            "with `python scripts/generate_secrets.py --api-key`.",
        )

    from app.models.database import session_scope

    with session_scope() as db:
        tenant = tenancy.get_tenant_by_slug(db, settings.bootstrap_tenant_slug)
        if tenant is None:
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                f"Bootstrap tenant {settings.bootstrap_tenant_slug!r} does not exist. "
                f"Create it with `python -m app.cli bootstrap`.",
            )
        return Actor(
            actor_type=ActorType.USER,
            actor_id="bootstrap-api-key",
            tenant_id=tenant.tenant_id,
            role=Role.ADMIN,
            display_name="bootstrap",
            correlation_id="bootstrap",
        )


def resolve_actor(
    request: Request,
    authorization: Annotated[str | None, Header()] = None,
    x_api_key: Annotated[str | None, Header()] = None,
    x_device_id: Annotated[str | None, Header()] = None,
    x_device_secret: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db),
) -> Actor:
    """Turn whatever credential was presented into a verified :class:`Actor`.

    Tries, in order: user JWT, device credential, bootstrap API key. A failure
    in one is not a failure overall while another is still possible, so a
    request carrying both an expired token and a valid device secret succeeds
    on the device secret -- which is the normal case for a node that also holds
    an operator token it has rotated out.

    Raises:
        HTTPException: 401 when nothing presented verifies.
    """
    attempts: list[str] = []

    if authorization:
        token = _bearer(authorization)
        try:
            claims = decode_token(token)
        except InvalidCredentials as exc:
            attempts.append(f"user token: {exc}")
        else:
            user = tenancy.get_user(db, claims.tenant_id, claims.subject)
            if user is None:
                attempts.append("user token: the account no longer exists")
            elif not user.is_active:
                raise HTTPException(status.HTTP_403_FORBIDDEN, "This account is disabled.")
            elif security.token_is_valid_after(claims, user.tokens_valid_after) is False:
                # A password change invalidates every previously issued token.
                # Without this, "log out everywhere" on a compromised account
                # would be a no-op until the tokens expired on their own.
                attempts.append("user token: superseded by a password change")
            else:
                return Actor(
                    actor_type=ActorType.USER,
                    actor_id=user.user_id,
                    tenant_id=user.tenant_id,
                    role=claims.role,
                    display_name=user.display_name or user.email,
                    correlation_id=claims.jti or "",
                )

    if x_device_id or x_device_secret:
        device_id, secret = _device_secret(x_device_id, x_device_secret)
        device = tenancy.find_device_by_credential(db, security.hash_secret(secret))
        if device is None or not security.verify_secret(secret, device.credential_hash):
            # Constant-time compare happens inside verify_secret; the branch
            # above is the "no such device" case.
            attempts.append("device credential: unknown device")
        elif device.device_id != device_id:
            attempts.append("device credential: device id does not match the secret")
        elif device.status != DEVICE_ACTIVE:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f"Device is {device.status}; it must be {DEVICE_ACTIVE} to upload.",
            )
        else:
            return Actor(
                actor_type=ActorType.DEVICE,
                actor_id=device.device_id,
                tenant_id=device.tenant_id,
                role=Role.READONLY,
                display_name=device.name or device.device_id,
                correlation_id=request.headers.get("X-Correlation-Id", ""),
                scopes=frozenset(device.scopes_list()),
            )

    if x_api_key:
        from app.core.security import require_api_key

        require_api_key(x_api_key)
        return _bootstrap_api_key(x_api_key)

    raise HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "No valid credential presented.",
        headers={"WWW-Authenticate": "Bearer"},
    ) if not attempts else HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "No valid credential presented: " + "; ".join(attempts),
        headers={"WWW-Authenticate": "Bearer"},
    )


def current_actor(actor: Actor = Depends(resolve_actor)) -> Actor:
    """FastAPI dependency exposing the verified actor."""
    return actor


def current_tenant(actor: Actor = Depends(resolve_actor)) -> TenantContext:
    """FastAPI dependency exposing a verified tenant scope.

    This is what handlers depend on instead of accepting a tenant id.
    """
    return actor.as_tenant_context()


def require(capability: str) -> Callable[[TenantContext], TenantContext]:
    """Build a dependency that enforces one capability.

    Usage::

        @router.post("/review/{review_id}/resolve")
        def resolve(ctx: Scope = Depends(require("review:resolve"))) -> ...

    :class:`PermissionDenied` is translated to a 403 here rather than in each
    handler. Letting it escape as a 500 is not merely untidy: it tells the
    caller "retry, it might work", and it puts a stack trace in the response
    body of a request that failed an authorisation check.
    """

    def _dependency(ctx: TenantContext = Depends(current_tenant)) -> TenantContext:
        try:
            ctx.actor.require(capability)
        except PermissionDenied as exc:
            log.warning(
                "capability denied",
                extra={
                    "stage": "rbac",
                    "actor_id": ctx.actor.actor_id,
                    "actor_type": ctx.actor.actor_type.value,
                    "role": ctx.actor.role.value,
                    "capability": capability,
                },
            )
            raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc
        return ctx

    return _dependency


def enforce_tenant(ctx: TenantContext, entity: object, resource: str) -> str:
    """Assert a loaded row belongs to the caller's tenant.

    Turns a :class:`TenantViolation` into a 403 with a message that names the
    resource but never leaks the other tenant's identifier: a 404 would hide
    existence, but the operator needs to know they asked for something that is
    not theirs, and the other tenant's id is not the useful part of that.
    """
    try:
        ctx.assert_entity(entity)
    except TenantViolation as exc:
        log.warning(
            "cross-tenant access refused",
            extra={
                "stage": "tenant_guard",
                "actor_id": ctx.actor.actor_id,
                "resource": resource,
            },
        )
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            f"This {resource} does not belong to your organisation.",
        ) from exc
    return ctx.tenant_id


#: Plain alias. Route signatures use ``Scope`` as a *parameter type* and
#: ``Depends(require("..."))`` as its default, because FastAPI forbids
#: ``Depends`` appearing in both an ``Annotated`` metadata and the default.
Scope = TenantContext

#: FastAPI dependencies for the common case: a plain verified tenant, or the
#: verified actor itself.
TenantCtx = Annotated[TenantContext, Depends(current_tenant)]
ActorDep = Annotated[Actor, Depends(current_actor)]
DbDep = Annotated[Session, Depends(get_db)]

def require_upload(capability: str = "session:write") -> Callable[[TenantContext], TenantContext]:
    """Build a dependency for endpoints both a person and a camera may call.

    Frame upload is the one endpoint with two legitimate callers: a teacher
    uploading a photo by hand, and an edge node streaming captures. Checking
    only a human capability locks the camera out; checking only a scope lets a
    compromised classroom device do anything an operator scoped it to by
    mistake. So each actor type is checked against its own credential:

    * a device must carry the upload scope;
    * a person must hold the capability.

    Raises:
        HTTPException: 403 for either failure.
    """

    def _dependency(ctx: TenantContext = Depends(current_tenant)) -> TenantContext:
        try:
            if ctx.actor.is_device:
                ctx.actor.require_scope(DEVICE_UPLOAD_SCOPE)
            else:
                ctx.actor.require(capability)
        except PermissionDenied as exc:
            log.warning(
                "upload refused",
                extra={
                    "stage": "rbac",
                    "actor_id": ctx.actor.actor_id,
                    "actor_type": ctx.actor.actor_type.value,
                    "capability": capability,
                },
            )
            raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc
        return ctx

    return _dependency


__all__ = [
    "DEVICE_UPLOAD_SCOPE",
    "ActorDep",
    "DbDep",
    "Scope",
    "TenantCtx",
    "current_actor",
    "current_tenant",
    "enforce_tenant",
    "get_db",
    "require",
    "require_upload",
    "resolve_actor",
]
