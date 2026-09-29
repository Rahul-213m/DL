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
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging
from app.models.database import SessionLocal, assert_no_tables_in_production, session_scope
from app.registry.loader import load_registry
from app.services.gallery import gallery_index

configure_logging()

#: Alembic revision this build expects. Bumped by every schema change.
EXPECTED_SCHEMA_REVISION = "0001_initial_schema"


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Manage application startup and shutdown."""
    # Fail fast on an impossible configuration.
    settings.validate_invariants()

    # Load the model registry and enforce commercial licensing in production.
    registry = load_registry()

    # Never create tables implicitly. In production this is a hard check.
    assert_no_tables_in_production(EXPECTED_SCHEMA_REVISION)

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
    version="2.0.0",
    description=(
        "Cloud perception, identity resolution and operator console for autonomous classroom attendance."
    ),
    docs_url=None,
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/docs", include_in_schema=False)
def custom_docs() -> object:
    """Swagger UI, served from a pinned CDN version."""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Docs",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/health")
def health() -> dict[str, object]:
    """Liveness probe. Cheap: does not touch the database."""
    return {
        "status": "ok",
        "environment": settings.environment,
        "gallery_size": gallery_index.size,
        "schema_revision": EXPECTED_SCHEMA_REVISION,
    }


__all__ = ["SessionLocal", "app"]
