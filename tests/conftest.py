"""Pytest configuration shared by every job.

Two jobs run this suite:

* ``cloud`` — Python 3.13, no rclpy, no ROS. Runs ``tests/``.
* ``edge``  — Python 3.12 with ROS 2 Jazzy sourced. Runs ``ros_ws/src/*/test``.

Both import this file, so the ROS packages are only collected when rclpy is
actually importable. Previously a bare ``pytest`` at the repo root failed at
*collection* with ``ModuleNotFoundError: No module named 'rclpy'``, which meant
the entire suite was unrunnable on a developer machine that had not sourced ROS.
See docs/00_audit.md and W1 in docs/PROGRESS.md.
"""

from __future__ import annotations

import os
import tempfile

# Must be set before any app module is imported, because app.core.config reads
# the environment at import time. Tests must never touch the developer's real
# attendance.db, their ENROLL_PHOTOS tree, or their .env.
os.environ.setdefault("DATABASE_URL", "sqlite://")
_TEST_ROOT = tempfile.mkdtemp(prefix="attendance-tests-")
os.environ.setdefault("STORAGE_ROOT", os.path.join(_TEST_ROOT, "data"))
os.environ.setdefault("ENROLLMENT_PHOTOS_ROOT", os.path.join(_TEST_ROOT, "ENROLL_PHOTOS"))
# Never let a developer's shell config leak into the suite.
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.pop("MODEL_REGISTRY_CONFIG", None)

# Settings has no API_KEY default on purpose (a secret must be supplied, not
# inherited from a code default), so the suite supplies its own known key.
os.environ.setdefault("API_KEY", "test-only-key-not-a-real-secret")
os.environ.setdefault("JWT_SECRET", "test-only-jwt-secret-not-a-real-secret-0123456789")


def _ensure_legacy_schema() -> None:
    """Create the pre-tenant tables.

    The legacy schema and the multi-tenant schema live on separate declarative
    bases so their table names do not collide, which means each test suite must
    ask for the one it needs. Doing it here keeps it out of the tests.
    """
    from app.models.database import engine
    from app.models.schema import LegacyBase

    LegacyBase.metadata.create_all(engine, checkfirst=True)


def _ensure_tenancy_schema() -> None:
    """Create the multi-tenant tables.

    The import MUST come first: tables register themselves on
    ``Base.metadata`` when their module is imported, so importing
    ``Base`` alone leaves the metadata empty and ``create_all`` silently
    creates nothing.
    """
    import app.models.tenancy  # noqa: F401  (registers the tables)
    from app.models.database import Base, engine

    Base.metadata.create_all(engine, checkfirst=True)


#: True when a ROS 2 environment is available. Gates edge test collection.
ROS_AVAILABLE = False
try:  # pragma: no cover - environment dependent
    import rclpy  # noqa: F401

    ROS_AVAILABLE = True
except ImportError:
    ROS_AVAILABLE = False


# Both schemas exist in one in-memory database. The legacy tables back the 23
# original behavioural tests; the tenancy tables back the W4+ suites.
_ensure_legacy_schema()
_ensure_tenancy_schema()
