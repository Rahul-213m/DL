"""Device scopes, a real consent ledger, and rosters that hold more than one student.

Revision ID: 0003_device_scopes_and_roster_fixes
Revises: 0002_multi_tenancy

Three schema changes, all of which the ORM models had already started to
assume. 0002 generated its DDL from the ORM metadata, so on any database that
already applied it these three things are absent while the code depends on them
-- which is the exact failure ``create_all``-era code had, and the reason
production refuses to run without a migration.

1. ``devices.scopes``
   A device credential is upload-only unless it says otherwise. That was
   enforced in Python, which means a row inserted by a migration, an admin
   script, or a future code path would default to *no* scopes at best and to
   whatever the model happened to say at worst. The column plus a server
   default makes the safe value the one you get by doing nothing.

2. Drop ``uq_class_tenant_class`` from ``class_members``
   A unique constraint on (tenant_id, class_id) means one student per class.
   The same constraint name is also correct on the ``classes`` table, where it
   keeps a class code unique within a tenant, so this drops by *table* and
   leaves that one alone.

3. Drop ``uq_consent_tenant_student`` from ``consent_records``
   One row per student cannot represent a history. Withdrawing and then
   re-granting had to either overwrite the grant or fail, and an append-only
   ledger is the only version that can answer "was this person ever consented",
   which is the question an audit asks.

All three are destructive to constraint, never to data: nothing is deleted, and
the downgrade restores the constraints only when the data would still satisfy
them. Re-adding a unique constraint over rows that violate it would fail
mid-rollback and leave the database in a state neither revision describes.
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_device_scopes_and_roster_fixes"
down_revision: str | None = "0002_multi_tenancy"

branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

#: What a device may do when nothing says otherwise. Deliberately the smallest
#: useful set: a classroom computer uploads frames and does nothing else.
DEFAULT_DEVICE_SCOPES = '["frames:upload"]'


def _has_table(name: str) -> bool:
    return bool(sa.inspect(op.get_bind()).has_table(name))


def _has_column(table: str, column: str) -> bool:
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table(table):
        return False
    return any(found["name"] == column for found in inspector.get_columns(table))


def _has_constraint(table: str, name: str) -> bool:
    """Whether a unique constraint of this name exists on this table.

    Checked rather than assumed, because this revision is expected to be
    re-runnable after a partial apply. Dropping a constraint that is not there
    aborts the transaction, and aborting halfway through is how a database
    ends up with the new column and the old constraints.
    """
    inspector = sa.inspect(op.get_bind())
    if not inspector.has_table(table):
        return False
    for constraint in inspector.get_unique_constraints(table):
        if constraint.get("name") == name:
            return True
    # SQLite reports unique constraints created as UNIQUE indexes.
    return any(
        index.get("name") == name and bool(index.get("unique"))
        for index in inspector.get_indexes(table)
    )


def _duplicates(table: str, columns: Sequence[str]) -> int:
    """How many row groups would violate the constraint we are about to add.

    The identifiers are literals in this file, never input, so the f-string is
    a readability trade rather than an injection surface. Text() keeps the
    dialect-neutral GROUP BY working on both PostgreSQL and SQLite.
    """
    bind = op.get_bind()
    listed = ", ".join(columns)
    query = sa.text(f"SELECT {listed} FROM {table} GROUP BY {listed} HAVING COUNT(*) > 1")  # noqa: S608
    return len(bind.execute(query).fetchall())


def upgrade() -> None:
    if _has_table("devices") and not _has_column("devices", "scopes"):
        op.add_column(
            "devices",
            sa.Column(
                "scopes",
                sa.Text(),
                nullable=False,
                server_default=DEFAULT_DEVICE_SCOPES,
            ),
        )
        # The default stays. An INSERT from a path that has not been updated
        # for this column should land on upload-only, not on NULL and not on
        # whatever a future model change decides.

    # batch_alter_table, not a bare drop_constraint: SQLite cannot ALTER a
    # constraint and needs the copy-and-move strategy. Dev and CI run on SQLite,
    # and a migration that only works on the production dialect is a migration
    # nobody has actually run.
    if _has_table("class_members") and _has_constraint("class_members", "uq_class_tenant_class"):
        with op.batch_alter_table("class_members") as batch:
            batch.drop_constraint("uq_class_tenant_class", type_="unique")

    if _has_table("consent_records") and _has_constraint(
        "consent_records", "uq_consent_tenant_student"
    ):
        with op.batch_alter_table("consent_records") as batch:
            batch.drop_constraint("uq_consent_tenant_student", type_="unique")


def downgrade() -> None:
    """Restore the constraints, but only where the data can still satisfy them.

    A downgrade that fails halfway leaves the database matching neither
    revision. Reporting the conflict is more useful than guessing which rows to
    delete, and biometric consent history is not this function's to discard.
    """
    if _has_table("consent_records") and not _has_constraint(
        "consent_records", "uq_consent_tenant_student"
    ):
        conflicts = _duplicates("consent_records", ["tenant_id", "student_id"])
        if conflicts:
            raise RuntimeError(
                f"cannot restore uq_consent_tenant_student: {conflicts} student(s) have more "
                "than one consent record. Keep the append-only ledger; the constraint is not "
                "compatible with a consent history."
            )
        with op.batch_alter_table("consent_records") as batch:
            batch.create_unique_constraint(
                "uq_consent_tenant_student", ["tenant_id", "student_id"]
            )

    if _has_table("class_members") and not _has_constraint(
        "class_members", "uq_class_tenant_class"
    ):
        conflicts = _duplicates("class_members", ["tenant_id", "class_id"])
        if conflicts:
            raise RuntimeError(
                f"cannot restore uq_class_tenant_class: {conflicts} class(es) have more than "
                "one member. That constraint is what limited a class to a single student."
            )
        with op.batch_alter_table("class_members") as batch:
            batch.create_unique_constraint("uq_class_tenant_class", ["tenant_id", "class_id"])

    if _has_table("devices") and _has_column("devices", "scopes"):
        with op.batch_alter_table("devices") as batch:
            batch.drop_column("scopes")
