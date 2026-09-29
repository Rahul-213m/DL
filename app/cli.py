"""Operator command line.

These are the commands an on-call engineer needs at 2am when the service will
not start. Each one prints the *reason* rather than a traceback.

    python -m app.cli check_licensing    # will this configuration ship?
    python -m app.cli check_config       # is the configuration self-consistent?
    python -m app.cli doctor             # everything, in one report
    python -m app.cli purge              # apply retention policies
    python -m app.cli reindex            # rebuild the vector index from the DB
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def _ok(message: str) -> None:
    print(f"  [ok]   {message}")


def _fail(message: str) -> None:
    print(f"  [FAIL] {message}")


def _warn(message: str) -> None:
    print(f"  [warn] {message}")


def cmd_check_config(_: argparse.Namespace) -> int:
    """Validate configuration invariants."""
    from app.core.config import Settings

    print("Configuration:")
    try:
        settings = Settings()
        settings.validate_invariants()
    except Exception as exc:
        _fail(str(exc))
        return 1
    _ok(f"environment={settings.environment}")
    _ok(f"database={_redact_db(settings.database_url)}")
    _ok(f"storage={settings.storage_backend}")
    _ok(f"queue={settings.job_queue_backend}")
    _ok(
        f"thresholds low={settings.low_confidence_threshold} "
        f"high={settings.high_confidence_threshold} margin={settings.match_margin_threshold}"
    )
    return 0


def cmd_check_licensing(_: argparse.Namespace) -> int:
    """Verify the configured models may lawfully serve a paying customer.

    Exit code 1 means the service would refuse to start in production. This is
    the check the CI release job runs.
    """
    from app.core.config import Settings
    from app.registry.models import ModelRegistry

    settings = Settings()
    print("Model licensing:")
    registry = ModelRegistry()
    registry.load_from_config(settings.model_registry_config)

    try:
        registry.assert_production_licensing(
            detector_key=settings.detector_backend,
            embedder_key=settings.embedder_backend,
            is_production=True,  # always evaluate as if shipping
        )
    except Exception as exc:
        _fail(str(exc))
        return 1

    for descriptor in registry.enabled_for_production(settings.detector_backend, settings.embedder_backend):
        _ok(
            f"{descriptor.key} ({descriptor.version}): {descriptor.license.license_name}, "
            f"commercial_use={descriptor.license.commercial_use}"
        )

    pending = registry.pending_legal_reviews()
    if pending:
        _warn(f"legal review outstanding for: {', '.join(pending)} (NEEDS LAWYER)")
        _warn("tracked in docs/HUMAN_ACTIONS.md; non-blocking by deliberate decision")
    return 0


def cmd_doctor(_: argparse.Namespace) -> int:
    """Run every self-check and summarise."""
    print("=" * 70)
    print("attendance-cloud doctor")
    print("=" * 70)

    failures = 0

    print("\n[1/4] configuration")
    failures += cmd_check_config(argparse.Namespace())

    print("\n[2/4] model licensing (evaluated as production)")
    failures += cmd_check_licensing(argparse.Namespace())

    print("\n[3/4] database")
    try:
        from app.models.database import healthcheck

        db = healthcheck()
        if db["database"]["status"] == "ok":
            _ok(f"reachable ({db['database']['dialect']})")
        else:
            _fail(str(db["database"]))
            failures += 1
    except Exception as exc:
        _fail(f"unreachable: {type(exc).__name__}: {exc}")
        failures += 1

    print("\n[4/4] schema revision")
    try:
        from app.main import EXPECTED_SCHEMA_REVISION
        from app.models.database import assert_schema_current

        assert_schema_current(EXPECTED_SCHEMA_REVISION)
        _ok(f"at {EXPECTED_SCHEMA_REVISION}")
    except Exception as exc:
        _fail(str(exc))
        failures += 1

    print("\n" + "=" * 70)
    if failures:
        print(f"RESULT: {failures} problem(s). The service will not start.")
        return 1
    print("RESULT: all checks passed.")
    return 0


def cmd_purge(args: argparse.Namespace) -> int:
    """Apply retention policies to stored images."""
    from app.retention import purge_expired

    result: dict[str, Any] = purge_expired(dry_run=not args.apply)
    mode = "DRY RUN" if not args.apply else "APPLIED"
    print(f"Retention purge ({mode}):")
    for scope, count in result["deleted"].items():
        print(f"  {scope:<24} {count} object(s)")
    if result["errors"]:
        for err in result["errors"]:
            _fail(err)
        return 1
    return 0


def cmd_reindex(_: argparse.Namespace) -> int:
    """Rebuild the vector index from the database, which is the source of truth."""
    from app.models.database import session_scope
    from app.services.gallery import gallery_index

    with session_scope() as db:
        size = gallery_index.rebuild(db)
    _ok(f"vector index rebuilt: {size} vectors")
    return 0


def cmd_models(_: argparse.Namespace) -> int:
    """Print the model registry as JSON (used by the health endpoint)."""
    from app.registry.models import ModelRegistry

    print(json.dumps([_descriptor_row(d) for d in ModelRegistry()], indent=2, default=str))
    return 0


def _descriptor_row(descriptor: Any) -> dict[str, Any]:
    """Flatten a descriptor for JSON output."""
    return {
        "key": descriptor.key,
        "kind": descriptor.kind,
        "version": descriptor.version,
        "license": descriptor.license.license_name,
        "commercial_use": descriptor.license.commercial_use,
        "training_data": descriptor.license.training_data,
        "source_url": descriptor.license.source_url,
        "sha256": descriptor.license.sha256,
        "embedding_dimension": descriptor.embedding_dimension,
        "shippable": descriptor.shippable,
        "legal_review_required": descriptor.license.legal_review_required,
    }


def _redact_db(url: str) -> str:
    """Strip credentials from a database URL before printing it."""
    if "@" not in url:
        return url
    scheme, _, rest = url.partition("://")
    _, _, host = rest.rpartition("@")
    return f"{scheme}://***@{host}"


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(prog="attendance", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("check_config", help="validate configuration invariants").set_defaults(
        func=cmd_check_config
    )
    sub.add_parser(
        "check_licensing", help="verify the models may lawfully serve a paying customer"
    ).set_defaults(func=cmd_check_licensing)
    sub.add_parser("doctor", help="run every self-check").set_defaults(func=cmd_doctor)
    sub.add_parser("reindex", help="rebuild the vector index from the database").set_defaults(
        func=cmd_reindex
    )
    sub.add_parser("models", help="print the model registry as JSON").set_defaults(func=cmd_models)

    purge = sub.add_parser("purge", help="apply retention policies to stored images")
    purge.add_argument("--apply", action="store_true", help="actually delete (default is a dry run)")
    purge.set_defaults(func=cmd_purge)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
