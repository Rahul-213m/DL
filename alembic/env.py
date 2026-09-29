"""Alembic environment for the attendance cloud service.

The database URL is taken from application settings (and therefore from the
environment / ``.env``) rather than from ``alembic.ini``. That keeps a single
source of truth: migrations always target the database the app will actually
use.

Why Alembic is the ONLY schema path
-----------------------------------
The original code called ``Base.metadata.create_all()`` at startup. ``create_all``
cannot ALTER an existing table, so any schema change silently applied only to
fresh databases while deployed databases kept the old shape. See
docs/00_audit.md §6.5. ``app.core.database`` now refuses to create tables in
production; use ``alembic upgrade head``.
"""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings

# Importing the models module registers every table on Base.metadata.
# Alembic cannot autogenerate against metadata it has never seen.
from app.models import schema  # noqa: F401  (registers tables on Base.metadata)
from app.models.database import Base

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Emit SQL to stdout without connecting (``alembic upgrade --sql``)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Apply migrations against a live connection."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            # Required for SQLite, which cannot ALTER most things in place.
            render_as_batch=connection.dialect.name == "sqlite",
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
