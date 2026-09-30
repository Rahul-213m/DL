#!/usr/bin/env python3
"""Calibrate the recognition thresholds against stored, human-labelled evidence.

WHAT THIS PRODUCES
------------------
A table of operating points (TAR / FAR / FRR) and one recommendation for
``HIGH_CONFIDENCE_THRESHOLD`` and ``LOW_CONFIDENCE_THRESHOLD``, measured from
the evidence in your database.

WHAT IT WILL NOT PRODUCE
------------------------
A number you can quote as accuracy if you have no labelled data yet. In that
case it says so and exits non-zero, because a threshold derived from nothing is
worse than no threshold: it looks measured.

WHY ONLY HUMAN-LABELLED EVIDENCE
--------------------------------
Auto-confirmed events are excluded. Calibrating on the matcher's own output
measures the thresholds rather than testing them, and would flatter the system
exactly where it is weakest. See ``app/services/calibration.py``.

USAGE
-----
    python scripts/calibrate_thresholds.py --tenant <slug>
    python scripts/calibrate_thresholds.py --all-tenants --far-target 0.001
    python scripts/calibrate_thresholds.py --tenant acme --json out.json

The recommendation is applied with:

    HIGH_CONFIDENCE_THRESHOLD=<value> LOW_CONFIDENCE_THRESHOLD=<value> \\
        python -m app.cli doctor
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.domain.calibration import roc_auc
from app.models.database import SessionLocal
from app.services.calibration import calibrate_from_database


def _tenants(db: object, slug: str | None) -> list[tuple[str, str]]:
    """Resolve ``(tenant_id, slug)`` pairs to report on."""
    from sqlalchemy import select

    from app.models.tenancy import Tenant

    statement = select(Tenant.tenant_id, Tenant.slug)
    if slug:
        statement = statement.where(Tenant.slug == slug)
    return [(row.tenant_id, row.slug) for row in db.execute(statement).all()]  # type: ignore[attr-defined]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tenant", help="Tenant slug. Omit with --all-tenants to do every tenant.")
    parser.add_argument("--all-tenants", action="store_true", help="Report on every tenant.")
    parser.add_argument(
        "--far-target",
        type=float,
        default=0.001,
        help="False-accept rate the high threshold must not exceed (default 0.001 = 0.1%%).",
    )
    parser.add_argument(
        "--low-keep-fraction",
        type=float,
        default=0.99,
        help="Share of genuine sightings the low threshold must keep, so that a "
        "real student at an awkward angle reaches a human instead of being "
        "discarded (default 0.99). Lower it only to reduce operator workload; "
        "the impostors it admits are reported.",
    )
    parser.add_argument("--json", type=Path, help="Also write the full report as JSON to this path.")
    parser.add_argument("--step", type=int, default=5, help="Show every Nth operating point (default 5).")
    args = parser.parse_args(argv)

    if not args.tenant and not args.all_tenants:
        parser.error("pass --tenant SLUG or --all-tenants")

    payload: dict[str, object] = {"far_target": args.far_target, "tenants": {}}
    exit_code = 0

    with SessionLocal() as db:
        tenants = _tenants(db, args.tenant)
        if not tenants:
            print("No matching tenant. Create one first (see docs/operator_guide.md).")
            return 2

        for tenant_id, slug in tenants:
            report, populations = calibrate_from_database(
                db,
                tenant_id,
                far_target=args.far_target,
                low_keep_fraction=args.low_keep_fraction,
            )
            auc = roc_auc(populations.positives, populations.negatives)

            print(f"\n=== tenant: {slug} ({tenant_id}) ===")
            print(f"  labelled sightings   : {populations.labelled_sightings}")
            print(f"  gallery identities   : {populations.gallery_students}")
            print(f"  positive scores      : {len(populations.positives)}")
            print(f"  negative scores      : {len(populations.negatives)}")
            print(f"  excluded (auto)      : {populations.excluded_auto}")
            print(f"  ROC AUC              : {auc:.4f}" if auc == auc else "  ROC AUC              : n/a")
            if populations.by_distance:
                print("  positives by face size:")
                for bucket, scores in sorted(populations.by_distance.items()):
                    low = min(scores)
                    print(f"      {bucket:<10} n={len(scores):<6} min={low:.4f}")
            print()
            print(report.table(step=args.step))
            print()
            print(f"  RECOMMENDED HIGH_CONFIDENCE_THRESHOLD = {report.recommended_high:.4f}")
            print(f"  RECOMMENDED LOW_CONFIDENCE_THRESHOLD  = {report.recommended_low:.4f}")
            print(
                f"  low threshold keeps {report.kept_fraction:.2%} of genuine sightings "
                f"and sends {report.negatives_above_low} impostor comparisons to review"
            )
            for warning in report.warnings:
                print(f"  WARNING: {warning}")

            if not populations.positives or not populations.negatives:
                print(
                    "\n  NOT ENOUGH LABELLED DATA to calibrate. Resolve some review "
                    "items by hand (the operator console does this in one click), or "
                    "follow docs/data_collection_protocol.md."
                )
                exit_code = 3

            payload["tenants"][slug] = {  # type: ignore[index]
                "tenant_id": tenant_id,
                "report": report.as_dict(),
                "populations": populations.as_dict(),
                "roc_auc": auc if auc == auc else None,
            }

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\nwrote {args.json}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
