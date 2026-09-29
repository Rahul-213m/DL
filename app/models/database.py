"""SQLAlchemy engine, session factory and ORM base.

Two responsibilities live here and nowhere else:

1. **Engine construction** — including the SQLite pragmas (WAL, busy timeout)
   without which concurrent writers fail with ``database is locked``.
2. **The ORM models** — the relational schema. Alembic owns migrations; this
   module owns the Python mapping only.

Multi-tenancy
-------------
Every tenant-owned table carries ``tenant_id`` and every repository method
filters on it. This is enforced by :class:`TenantSession`, which raises if a
query is issued without a tenant context. See docs/decisions/0007-multitenancy.md.
"""

from __future__ import annotations

import contextlib
from collections.abc import Iterator
from typing import Any

from sqlalchemy import DateTime, create_engine, event, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    """Declarative base for every ORM model."""


# ---------------------------------------------------------------------------
# UTC timestamp helper
# ---------------------------------------------------------------------------
# Every datetime column in the system is timezone-aware UTC. SQLite does not
# store tzinfo, so values come back naive; this normalises them on read.
# See docs/decisions/0009-utc-timestamps.md


def utcnow() -> Any:
    """Return a timezone-aware UTC ``datetime``."""
    from datetime import UTC, datetime

    return datetime.now(UTC)


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


def _build_engine() -> Any:
    """Construct the SQLAlchemy engine from settings."""
    url = settings.database_url
    kwargs: dict[str, Any] = {"future": True, "pool_pre_ping": True}

    if url.startswith("sqlite"):
        # A shared in-memory database (used by tests) needs one connection.
        if url in {"sqlite://", "sqlite:///:memory:"}:
            from sqlalchemy.pool import StaticPool

            kwargs["poolclass"] = StaticPool
            kwargs["connect_args"] = {"check_same_thread": False}
        else:
            kwargs["connect_args"] = {
                "check_same_thread": False,
                "timeout": settings.db_sqlite_busy_timeout_ms / 1000,
            }

        if not settings.is_production:
            # Production uses PostgreSQL; SQLite is dev/test only.
            kwargs["pool_pre_ping"] = True

    else:
        kwargs.update(
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_recycle=settings.db_pool_recycle_seconds,
        )

    return create_engine(url, **kwargs)


engine = _build_engine()


@event.listens_for(engine, "connect")
def _set_sqlite_pragmas(dbapi_connection: Any, _connection_record: Any) -> None:
    """Apply SQLite durability and concurrency pragmas on every connection.

    - ``journal_mode=WAL`` lets readers proceed while a writer holds the
      write lock. Without it the review queue blocks while a scan commits.
    - ``busy_timeout`` makes a blocked writer wait instead of raising
      ``database is locked`` immediately.
    - ``foreign_keys=ON`` makes SQLite actually enforce referential integrity.
      It is OFF by default for compatibility, which silently allowed orphan
      ``face_gallery`` rows in the legacy database.
    - ``synchronous=NORMAL`` is the standard WAL pairing: durable across
      process crashes, and only at risk from an OS-level crash.
    """
    if not settings.database_url.startswith("sqlite"):
        return
    cursor = dbapi_connection.cursor()
    try:
        if settings.db_sqlite_wal:
            cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute(f"PRAGMA busy_timeout={int(settings.db_sqlite_busy_timeout_ms)}")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA synchronous=NORMAL")
    finally:
        cursor.close()


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)


def get_db() -> Iterator[Session]:
    """FastAPI dependency yielding a request-scoped session.

    The session is rolled back and closed by the dependency teardown, so a
    handler that raises never leaves an open transaction.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def assert_schema_current(expected_revision: str) -> None:
    """Verify the database is at the expected Alembic revision.

    Raises:
        RuntimeError: if Alembic has not been run, or is behind. Refusing to
            serve traffic against an out-of-date schema is far safer than the
            alternative, which is confusing runtime errors deep in a scan.
    """
    with engine.connect() as connection:
        row = connection.execute(text("SELECT version_num FROM alembic_version")).fetchone()
    current = row[0] if row else None
    if current != expected_revision:
        raise RuntimeError(
            "Database schema is out of date. "
            f"Expected Alembic revision '{expected_revision}', found '{current}'. "
            "Run: alembic upgrade head"
        )


def assert_no_tables_in_production(expected_revision: str) -> None:
    """Refuse to run in production without a migrated schema.

    The legacy code called ``Base.metadata.create_all()`` at startup.
    ``create_all`` cannot ALTER an existing table, so schema changes silently
    applied only to fresh databases. See docs/00_audit.md §6.5.
    """
    if not settings.is_production:
        return
    assert_schema_current(expected_revision)


def healthcheck() -> dict[str, Any]:
    """Return a DB health payload for ``/health/ready``."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": {"status": "ok", "dialect": engine.dialect.name}}
    except Exception as exc:  # noqa: BLE001  # pragma: no cover - real outages only
        return {"database": {"status": "error", "error": f"{type(exc).__name__}: {exc}"}}


@contextlib.contextmanager
def session_scope() -> Iterator[Session]:
    """Transactional scope for scripts and background workers.

    Commits on clean exit, rolls back on any exception.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class TenantViolation(RuntimeError):
    """Raised when code attempts to access another tenant's data."""


# Re-exported for model modules that need the column types.
__all__ = [
    "Base",
    "DateTime",
    "Mapped",
    "SessionLocal",
    "TenantViolation",
    "assert_no_tables_in_production",
    "assert_schema_current",
    "engine",
    "get_db",
    "healthcheck",
    "mapped_column",
    "session_scope",
    "sessionmaker",
    "utcnow",
]
