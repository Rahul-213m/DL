from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from app.api.routes import router
from app.core.logging import configure_logging
from app.models.database import SessionLocal, init_db
from app.services.gallery import gallery_index

configure_logging()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        gallery_index.rebuild(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="AI Classroom Attendance",
    version="1.0.0",
    docs_url=None,
    lifespan=lifespan,
)
app.include_router(router)
@app.get("/docs", include_in_schema=False)
def custom_docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Docs",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
    )
@app.get("/health")
def health():
    return {"status": "ok"}
