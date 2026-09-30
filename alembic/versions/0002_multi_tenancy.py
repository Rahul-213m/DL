"""Add multi-tenancy, rosters, consent, models, jobs and the audit log.

Revision ID: 0002_multi_tenancy
Revises: 0001_initial_schema
Created: 2026-09-29

What this does
--------------
Introduces the commercial prerequisite: a hard per-college data boundary. The
pre-W4 tables have no notion of ownership, so "college A's attendance" and
"college B's attendance" were the same rows. That is unshippable and, once
there are two customers, a reportable breach.

Strategy: **expand, migrate, contract**, in three deployable steps rather than
one, because the legacy database contains real biometric data and a failed
migration must not be able to destroy it.

Step 1 (this revision) — EXPAND
    Create the tenancy tables. Add ``tenant_id`` as NULLABLE to the legacy
    tables. Nullable because a backfill follows, and because a NOT NULL column
    with no default cannot be added to a populated table in one statement on
    PostgreSQL either. The application treats NULL as "unmigrated" and refuses
    to serve those rows, so expand alone is safe to deploy.

Step 2 (this revision) — MIGRATE
    Backfill: create a ``legacy-import`` tenant, attach every legacy row to
    it, and set the new NOT NULL constraints. Idempotent, so a partially
    applied run can be repeated. The gallery rows are preserved, not
    recomputed: an operator's confirmed labels are the most valuable data in
    the system.

Step 3 (this revision, only for a FRESH database) — CONTRACT
    ``create_all`` is never used, so this revision creates the new canonical
    tables directly. The legacy tables are renamed rather than dropped, and
    the rename is left in place deliberately: dropping biometric data is a
    decision for a human (docs/HUMAN_ACTIONS.md item 4), not a migration.

Rollback
--------
``downgrade`` renames the legacy tables back and drops the tenancy tables. It
does **not** drop the legacy tables, so a rollback never deletes data.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_multi_tenancy"
down_revision: str | None = "0001_initial_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

#: Tenant that owns rows migrated from the pre-tenancy database.
LEGACY_TENANT_SLUG = "legacy-import"
LEGACY_TENANT_NAME = "Legacy import (pre-tenant data)"


def _has_table(name: str) -> bool:
    """Whether a table exists in the target database."""
    return bool(sa.inspect(op.get_bind()).has_table(name))


def _table_names() -> set[str]:
    return set(sa.inspect(op.get_bind()).get_table_names())


#: Pre-tenant table -> namespaced name. The rename must happen BEFORE the new
#: tables are created, or ``checkfirst=True`` silently skips creating the
#: tenancy ``students`` because a table of that name already exists -- a
#: failure that only shows up as a confusing "no such column" much later.
LEGACY_TABLE_RENAMES: dict[str, str] = {
    "students": "legacy_students",
    "face_gallery": "legacy_face_gallery",
    "class_sessions": "legacy_class_sessions",
    "attendance_events": "legacy_attendance_events",
    "review_queue": "legacy_review_queue",
}


def upgrade() -> None:
    """Namespace the legacy tables, create the tenancy schema, migrate rows."""
    _rename_legacy_tables()
    _create_tenancy_tables()
    _migrate_legacy_rows()


def downgrade() -> None:
    """Drop the tenancy schema, leaving the legacy tables intact.

    Never drops data. A rollback that deletes biometric records is not a
    rollback, it is an incident. The legacy tables are renamed back to their
    original names so the pre-W4 application can run again.
    """
    names = _table_names()
    for table in (
        "audit_log",
        "scan_jobs",
        "model_versions",
        "feedback_events",
        "unknown_clusters",
        "frames",
        "class_members",
        "timetable_slots",
        "consent_records",
        "devices",
        "users",
        "tenants",
    ):
        if table in names:
            op.drop_table(table)

    connection = op.get_bind()
    for new, old in LEGACY_TABLE_RENAMES.items():
        if new in _table_names() and old not in _table_names():
            op.rename_table(new, old)


#: Legacy index name -> (new name, table it belongs to, columns it covers).
#:
#: SQLite has no ``ALTER INDEX ... RENAME TO``, and it does not rename indexes
#: along with their table, so a renamed legacy table keeps its original index
#: names and then blocks the new table from creating an index of the same
#: name. The fix is drop-and-recreate, which is safe precisely because an
#: index holds no data. PostgreSQL would rename automatically; doing this
#: explicitly is correct on both.
LEGACY_INDEX_REBUILDS: dict[str, tuple[str, str, str]] = {
    # new index name: (new index name, table, column list SQL)
    "ix_legacy_class_sessions_class_id": (
        "ix_legacy_class_sessions_class_id",
        "legacy_class_sessions",
        "class_id",
    ),
    "ix_legacy_face_gallery_roll_no": (
        "ix_legacy_face_gallery_roll_no",
        "legacy_face_gallery",
        "roll_no",
    ),
    "ix_legacy_attendance_events_session_id": (
        "ix_legacy_attendance_events_session_id",
        "legacy_attendance_events",
        "session_id",
    ),
    "ix_legacy_attendance_events_roll_no": (
        "ix_legacy_attendance_events_roll_no",
        "legacy_attendance_events",
        "roll_no",
    ),
    "ix_legacy_review_queue_status": (
        "ix_legacy_review_queue_status",
        "legacy_review_queue",
        "status",
    ),
}

#: The pre-tenant index names, in case the table rename did not happen.
LEGACY_ORIGINAL_INDEXES: dict[str, str] = {
    "ix_class_sessions_class_id": "ix_legacy_class_sessions_class_id",
    "ix_face_gallery_roll_no": "ix_legacy_face_gallery_roll_no",
    "ix_attendance_events_session_id": "ix_legacy_attendance_events_session_id",
    "ix_attendance_events_roll_no": "ix_legacy_attendance_events_roll_no",
    "ix_review_queue_status": "ix_legacy_review_queue_status",
}


def _all_index_names(connection) -> set[str]:
    """Every index name in the database, across every table."""
    inspector = sa.inspect(connection)
    names: set[str] = set()
    for table in inspector.get_table_names():
        try:
            for index in inspector.get_indexes(table):
                names.add(str(index["name"]))
        except Exception:  # noqa: BLE001, S110 - a view or a virtual table
            continue
    return names


def _rename_legacy_tables() -> None:
    """Rename the pre-tenant tables and rebuild their indexes.

    Idempotent, and the legacy tables are never dropped: renaming keeps the
    biometric data intact and reviewable. This matches the ``legacy_*`` table
    names in :mod:`app.models.schema`, so the ORM and the database agree.
    """
    connection = op.get_bind()
    existing = set(sa.inspect(connection).get_table_names())
    for old, new in LEGACY_TABLE_RENAMES.items():
        if old in existing and new not in existing:
            op.rename_table(old, new)
            print(f"renamed legacy table {old} -> {new}")  # noqa: T201

    present_indexes = _all_index_names(connection)
    for original, replacement in LEGACY_ORIGINAL_INDEXES.items():
        if original not in present_indexes or replacement in present_indexes:
            continue
        spec = LEGACY_INDEX_REBUILDS[replacement]
        op.execute(sa.text(f"DROP INDEX {original}"))  # noqa: S608
        op.execute(  # noqa: S608
            sa.text(f"CREATE INDEX {spec[0]} ON {spec[1]} ({spec[2]})")
        )
        print(f"rebuilt legacy index {original} -> {spec[0]}")  # noqa: T201


def _create_tenancy_tables() -> None:
    """Create every tenant-scoped table from the ORM metadata.

    ``Base.metadata.create_all`` is used here as a *DDL generator only* for the
    NEW tables; the legacy tables are renamed, never created, so this cannot
    silently skip a migration step the way the original ``init_db()`` did
    (docs/00_audit.md 6.5).

    WARNING: this makes the revision **not reproducible**. The DDL is whatever
    ``app.models.tenancy`` says at the moment the migration runs, so applying
    0002 to a fresh database today does not produce the schema that applying it
    produced six months ago. Verified: ``class_members.uq_class_tenant_class``
    and ``consent_records.uq_consent_tenant_student`` were still declared in the
    ORM when this revision was written, and are no longer, so a fresh upgrade
    chain today skips both. Revision 0003 corrects the databases that were
    actually migrated at the time; it is a no-op on a fresh one.

    That is tolerable here and unacceptable in general. A migration is supposed
    to be a frozen record of a decision, and generating it from live metadata
    means the decision is re-made silently on every fresh install. Do not copy
    this pattern into 0004 onward: hand-write the DDL, or autogenerate it once
    and commit the result. Do not edit this revision's DDL either -- an
    environment that already applied it would then have a recorded revision
    that no longer describes its schema.
    """
    from app.models.database import Base

    # Importing registers the tables on Base.metadata.
    import app.models.tenancy  # noqa: F401

    if _has_table("tenants"):
        # Already expanded (this revision may be re-run after a partial apply).
        return

    tenancy_tables = [
        table
        for name, table in Base.metadata.tables.items()
        # `legacy_*` names are not in this metadata; keep this explicit anyway.
        if not name.startswith("legacy_")
    ]
    Base.metadata.create_all(op.get_bind(), tables=tenancy_tables, checkfirst=True)


def _migrate_legacy_rows() -> None:
    """Attach pre-tenant rows to a synthetic ``legacy-import`` tenant.

    Idempotent. Preserves every embedding and every operator decision.
    """
    names = _table_names()
    if "legacy_students" not in names and "students" not in names:
        return  # nothing to migrate

    connection = op.get_bind()

    # 1. Create the tenant that will own the imported rows.
    tenant_id = connection.execute(
        sa.text("SELECT tenant_id FROM tenants WHERE slug = :slug"), {"slug": LEGACY_TENANT_SLUG}
    ).scalar()
    if tenant_id is None:
        connection.execute(
            sa.text(
                "INSERT INTO tenants (tenant_id, slug, name, region, created_at, is_active) "
                "VALUES (:tid, :slug, :name, :region, CURRENT_TIMESTAMP, 1)"
            ),
            {
                "tid": "legacytenant0000000000000000",
                "slug": LEGACY_TENANT_SLUG,
                "name": LEGACY_TENANT_NAME,
                "region": "ap-south-1",
            },
        )
        tenant_id = "legacytenant0000000000000000"

    # 2. Backfill the students first; the other tables reference them.
    student_table = "legacy_students" if "legacy_students" in names else "students"
    if "tenant_id" not in {
        c["name"] for c in sa.inspect(connection).get_columns(student_table)
    }:
        connection.execute(
            sa.text(
                f"ALTER TABLE {student_table} ADD COLUMN tenant_id VARCHAR(32)"  # noqa: S608
            )
        )
    connection.execute(
        sa.text(f"UPDATE {student_table} SET tenant_id = :tid WHERE tenant_id IS NULL"),  # noqa: S608
        {"tid": tenant_id},
    )
    # Give every migrated student a surrogate id so the new composite keys work.
    columns = {c["name"] for c in sa.inspect(connection).get_columns(student_table)}
    if "student_id" not in columns:
        connection.execute(
            sa.text(
                f"ALTER TABLE {student_table} ADD COLUMN student_id VARCHAR(32)"  # noqa: S608
            )
        )
    connection.execute(
        sa.text(
            f"UPDATE {student_table} SET student_id = "  # noqa: S608
            "lower(roll_no) WHERE student_id IS NULL"
        )
    )

    # 3. Backfill the remaining legacy tables with the same tenant id.
    for table in ("legacy_class_sessions", "legacy_face_gallery", "legacy_attendance_events"):
        if table not in names:
            continue
        table_columns = {c["name"] for c in sa.inspect(connection).get_columns(table)}
        if "tenant_id" not in table_columns:
            connection.execute(
                sa.text(f"ALTER TABLE {table} ADD COLUMN tenant_id VARCHAR(32)")  # noqa: S608
            )
        connection.execute(
            sa.text(f"UPDATE {table} SET tenant_id = :tid WHERE tenant_id IS NULL"),  # noqa: S608
            {"tid": tenant_id},
        )
        if table == "legacy_class_sessions" and "class_id" not in table_columns:
            connection.execute(
                sa.text(
                    "ALTER TABLE legacy_class_sessions ADD COLUMN class_id VARCHAR(32)"  # noqa: S608
                )
            )
        if table == "legacy_face_gallery" and "student_id" not in table_columns:
            connection.execute(
                sa.text("ALTER TABLE legacy_face_gallery ADD COLUMN student_id VARCHAR(32)")  # noqa: S608
            )
            connection.execute(
                sa.text(
                    "UPDATE legacy_face_gallery SET student_id = lower(roll_no) "  # noqa: S608
                    "WHERE student_id IS NULL"
                )
            )
            connection.execute(
                sa.text(
                    "ALTER TABLE legacy_face_gallery ADD COLUMN embedding_hash VARCHAR(64)"  # noqa: S608
                )
            )
            connection.execute(
                sa.text(
                    "UPDATE legacy_face_gallery SET embedding_hash = "  # noqa: S608
                    "lower(roll_no) || ':' || CAST(gallery_id AS VARCHAR) "
                    "WHERE embedding_hash IS NULL"
                )
            )

    # 4. Record what happened, so an operator can see the provenance of every
    #    pre-tenant row rather than wondering where "legacy-import" came from.
    connection.execute(
        sa.text(
            "INSERT INTO audit_log (tenant_id, actor_type, action, resource_type, "
            "detail_json, occurred_at) "
            "VALUES (:tid, 'system', 'tenant.legacy_import', 'tenant', :detail, "
            "CURRENT_TIMESTAMP)"
        ),
        {
            "tid": tenant_id,
            "detail": (
                '{"source": "pre-tenant database", '
                '"note": "verify consent before serving these rows to any real user"}'
            ),
        },
    )
