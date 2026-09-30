"""FastAPI application entrypoint.

Startup order matters and is enforced here:

1. Logging is configured first so every later step is observable.
2. Configuration invariants are validated, so a misconfigured deployment dies
   immediately rather than at the first scan.
3. The **model registry** is loaded and the **production licensing guard** runs
   before any inference-capable object is constructed.
4. The schema revision is checked (never created) via Alembic.
5. The vector index is rebuilt from the database, which is the source of truth.
6. The detector/embedder are warmed so the first real request is not slow.

Nothing here is created implicitly in production. See docs/00_audit.md §6.5.
"""

from __future__ import annotations

import contextlib
import re
import threading
import time
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse

from app.api.routes import router as legacy_router
from app.api.routes_v1 import router as v1_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.models.database import SessionLocal, assert_no_tables_in_production, session_scope
from app.observability.metrics import configure_request_logging, correlation_id_var
from app.registry.loader import load_registry
from app.services.gallery import gallery_index
from app.services.tenant_index import tenant_indexes

configure_logging()
configure_request_logging()

#: Alembic revision this build expects. Bumped by every schema change.
#: The Alembic revision this build of the code requires. Kept as a literal so
#: that "the code changed but nobody migrated" is a startup failure rather than
#: a confusing runtime error. It must be bumped in the same commit as a change
#: to the models, and it is what ``alembic heads`` should print.
EXPECTED_SCHEMA_REVISION = "0003_device_scopes_and_roster_fixes"


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown."""
    # Fail fast on an impossible configuration.
    settings.validate_invariants()

    # Load the model registry and enforce commercial licensing in production.
    registry = load_registry()

    # Never create tables implicitly. In production this is a hard check.
    assert_no_tables_in_production(EXPECTED_SCHEMA_REVISION)

    with _LABEL_LOCK:
        _build_label_patterns_locked()

    # Rebuild the vector index from the database, which is the source of truth.
    with session_scope() as db:
        gallery_index.rebuild(db)

    # Warm the models so the first capture is not 30 seconds slower than the rest.
    # Inert for the default OpenCV backends, which load lazily per call.
    with contextlib.suppress(Exception):
        registry.warmup()

    yield

    # Release ONNX sessions and any pooled resources.
    with contextlib.suppress(Exception):
        registry.shutdown()


app = FastAPI(
    title="Attendance Cloud",
    version="3.0.0",
    description=(
        "Cloud perception, identity resolution and operator console for autonomous "
        "classroom attendance. The `/v1` surface is multi-tenant and scoped by "
        "verified credentials. The unprefixed surface is the legacy "
        "single-tenant API, kept for the edge bring-up window."
    ),
    docs_url=None,
    lifespan=lifespan,
)

# CORS: the operator console is normally served from a different host than the
# API, and a browser will refuse a cross-origin request without this. Origins
# are explicit rather than '*', because a wildcard plus credentials is refused
# by browsers anyway, and an explicit list is what stops a hostile site from
# making authenticated requests against a deployment that has credentials in
# local storage.
# Request instrumentation. The correlation id is generated here if the client
# did not send one, so every log line and every metric emitted while handling a
# request can be tied back to it -- including lines from code that never sees
# the request object.
@app.middleware("http")
async def instrument(
    request_obj: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Time every request and attach a correlation id to the response.

    The route *template* is recorded, never the concrete path. Labelling with
    ``/v1/sessions/17/register`` would mint a new time series per session and
    eventually take the metrics backend down; ``/v1/sessions/{session_id}`` is
    bounded no matter how much traffic the school generates.
    """
    from app.observability.metrics import request as record_request

    correlation_id = request_obj.headers.get("X-Correlation-Id") or uuid.uuid4().hex
    token = correlation_id_var.set(correlation_id)
    started = time.perf_counter()
    try:
        response = await call_next(request_obj)
    except Exception:
        # Record the failure before re-raising: a 500 that never reaches the
        # metrics is exactly the one an operator most needs to see.
        record_request(
            request_obj.method,
            _route_template(request_obj),
            500,
            time.perf_counter() - started,
        )
        raise
    finally:
        correlation_id_var.reset(token)
    response.headers["X-Correlation-Id"] = correlation_id
    record_request(
        request_obj.method,
        _route_template(request_obj),
        response.status_code,
        time.perf_counter() - started,
    )
    return response


#: (compiled path regex, canonical template) for every route, built once at
#: startup. Starlette reports a matched route's ``path`` *relative to the router
#: that declared it*, so ``/v1/review/{id}/resolve`` and the legacy
#: ``/review/{id}/resolve`` are both reported as ``/review/{id}/resolve``. Using
#: that directly would merge two unrelated endpoints into one time series.
_LABEL_PATTERNS: list[tuple[re.Pattern[str], str]] = []
#: ``id(route)`` -> canonical template. Learned on first sight, then free.
_LABEL_CACHE: dict[int, str] = {}
_LABEL_LOCK = threading.Lock()


def _build_label_patterns_locked() -> None:
    """Compile every declared path into a matcher. Caller holds the lock."""
    patterns: list[tuple[re.Pattern[str], str]] = []
    for template in app.openapi()["paths"]:
        pattern = re.sub(r"\{[^}]+\}", r"[^/]+", template)
        patterns.append((re.compile(f"^{pattern}$"), template))
    # Longest template first, so a specific route wins over a greedy one.
    patterns.sort(key=lambda item: len(item[1]), reverse=True)
    _LABEL_PATTERNS.clear()
    _LABEL_PATTERNS.extend(patterns)
    _LABEL_CACHE.clear()


def _route_template(request_obj: Request) -> str:
    """The canonical path template for this request, e.g. ``/v1/auth/me``.

    The concrete path is never used as a label unless nothing matched, because
    a label per session id is an unbounded time series: enough traffic would
    take the metrics backend down, and it is a cheap way for a client to do
    that deliberately. The unmatched case is truncated for the same reason.
    """
    route = request_obj.scope.get("route")
    path = request_obj.url.path
    if route is not None:
        key = id(route)
        cached = _LABEL_CACHE.get(key)
        if cached is not None:
            return cached
        with _LABEL_LOCK:
            if not _LABEL_PATTERNS:
                # Built lazily as well as at startup, so a process that never
                # ran the lifespan still labels correctly. Falling back to the
                # relative template would silently merge two endpoints.
                _build_label_patterns_locked()
            for pattern, template in _LABEL_PATTERNS:
                if pattern.match(path):
                    _LABEL_CACHE[key] = template
                    return template
            relative = getattr(route, "path", None)
            if isinstance(relative, str) and relative:
                _LABEL_CACHE[key] = relative
                return relative
    return path[:120]


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key", "X-Device-Id",
                   "X-Device-Secret", "X-Correlation-Id"],
    expose_headers=["X-Correlation-Id"],
    max_age=600,
)

app.include_router(v1_router)
app.include_router(legacy_router)


@app.get("/docs", include_in_schema=False)
def custom_docs() -> object:
    """Swagger UI, served from a pinned CDN version."""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url or "/openapi.json",
        title=app.title + " - Docs",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/health")
def health() -> dict[str, object]:
    """Liveness probe. Cheap: does not touch the database.

    A liveness probe that queries the database will restart a healthy process
    during a slow query, turning a degraded service into an unavailable one.
    Use ``/ready`` for anything that checks dependencies.
    """
    from app.services.tenant_index import tenant_indexes

    return {
        "status": "ok",
        "environment": settings.environment,
        # Legacy single-tenant index and the v1 per-tenant indexes are separate
        # stores, and the v1 API only ever searches the latter. Reporting one
        # number would hide a deployment whose v1 tenants were all enrolled but
        # whose tenant index was never warmed.
        "legacy_gallery_size": gallery_index.size,
        "tenant_indexed_identities": tenant_indexes.total_vectors(),
        "schema_revision": EXPECTED_SCHEMA_REVISION,
    }


@app.get("/ready")
def ready() -> Response:
    """Readiness probe. Checks the database, schema, models and gallery.

    Returns 503 when a dependency is unavailable so a load balancer stops
    sending traffic here, rather than every request failing individually.
    """
    from app.observability.metrics import readiness

    ok, detail = readiness()
    return JSONResponse(
        status_code=200 if ok else 503,
        content=detail,
    )


def _safe(read: Callable[[], int]) -> float:
    """A scrape must never 500. A -1 says "unknown", which is visibly wrong;
    an exception says only that the operator has no numbers at all."""
    try:
        return float(read())
    except Exception:  # noqa: BLE001
        return -1.0


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    """Prometheus metrics.

    Not behind auth: a scraper inside the cluster network needs to reach it
    without a credential, and the values are operational counters with no
    personal data. Deliberately free of student identifiers, roll numbers and
    tenant names -- a metrics backend is not a place for personal data, and
    aggregations are enough to operate the system.
    """
    from app.observability.metrics import registry

    # Aggregates only. The per-tenant breakdown names customers, and this
    # endpoint has no credential on it by design.
    for name, value in (
        ("attendance_gallery_size", _safe(lambda: gallery_index.size)),
        ("attendance_tenant_indexed_identities",
         _safe(lambda: tenant_indexes.total_vectors())),
    ):
        registry.gauge(
            name,
            "Identities in the live vector index (legacy global store)."
            if name == "attendance_gallery_size"
            else "Identities across all cached per-tenant vector indexes.",
            value,
        )
    return Response(content=registry.render(), media_type="text/plain; version=0.0.4")


__all__ = ["SessionLocal", "app"]
