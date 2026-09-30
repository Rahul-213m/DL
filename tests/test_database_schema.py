"""Schema readiness should report an absent migration table cleanly."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine

from app.models import database


def test_missing_alembic_version_is_reported_as_schema_revision_error(monkeypatch) -> None:
    isolated_engine = create_engine("sqlite://")
    monkeypatch.setattr(database, "engine", isolated_engine)

    with pytest.raises(database.SchemaRevisionError, match="found 'None'"):
        database.assert_schema_current("0003_device_scopes_and_roster_fixes")

    isolated_engine.dispose()
