#!/usr/bin/env python3
"""Verify model weight files against the SHA-256 recorded in the registry.

A swapped or corrupted weight file is a supply-chain incident, not a bug. The
registry records a hash per model; this script checks the bytes on disk
against it.

Exit codes:
    0 - every present weight file matches its recorded hash.
    1 - a hash mismatch (treated as a hard failure).
    2 - a weight file is missing (warning only; CI has no GPU/models).

Run standalone:  python scripts/verify_model_hashes.py
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.registry.models import BUILTIN_MODELS

MODELS_DIR = Path(__file__).resolve().parents[1] / "models"


def sha256_of(path: Path) -> str:
    """Return the hex SHA-256 of a file, streamed so memory stays flat."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    """Check every registered model whose weights file is present."""
    failures = 0
    checked = 0
    missing = 0

    for descriptor in BUILTIN_MODELS.values():
        if not descriptor.local_path:
            continue
        path = MODELS_DIR / descriptor.local_path
        recorded = descriptor.license.sha256

        if not path.is_file():
            print(f"SKIP  {descriptor.key}: {descriptor.local_path} not present")
            missing += 1
            continue

        actual = sha256_of(path)
        checked += 1
        if actual == recorded:
            print(f"OK    {descriptor.key}: {descriptor.local_path} {actual[:16]}...")
        else:
            print(
                f"FAIL  {descriptor.key}: {descriptor.local_path}\n"
                f"        recorded {recorded}\n"
                f"        actual   {actual}\n"
                "        A weight file does not match its recorded hash. Treat this as a "
                "supply-chain incident: do not run inference until it is resolved."
            )
            failures += 1

    print(f"\nchecked={checked} missing={missing} failures={failures}")
    if missing:
        print("Missing weights are expected on CI and on a fresh clone. See docs/model_licensing.md.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
