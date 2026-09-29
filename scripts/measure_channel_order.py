#!/usr/bin/env python3
"""Measure the channel-order defect on real classroom photographs.

The audit found (docs/00_audit.md 4.1) that the legacy pipeline fed RGB to
InsightFace, whose ONNX graphs expect BGR. This script quantifies what that
actually cost, on your own images, using two independent measures:

  1. SEPARABILITY  - mean same-person similarity minus mean different-person
     similarity, across every enrolled student. Higher is better. This is what
     the recognition threshold ultimately depends on.
  2. CONSISTENCY   - mean pairwise similarity among a single student's own
     photos, and the per-student spread. A wide spread means one photo of
     Priya matches another better than it matches its own gallery.

Usage:
    python scripts/measure_channel_order.py
    python scripts/measure_channel_order.py --photos ENROLL_PHOTOS --model insightface_buffalo_l
    python scripts/measure_channel_order.py --model opencv_sface

Every number printed is MEASURED on the images you pass, on the date printed.
Nothing here is extrapolated.
"""

from __future__ import annotations

import argparse
import statistics
import sys
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.domain.imageops import decode
from app.registry.loader import load_registry

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def collect_photos(root: Path, per_student: int) -> dict[str, list[Path]]:
    """Group images by their containing directory (one directory = one student)."""
    groups: dict[str, list[Path]] = {}
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        raise SystemExit(2)
    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        photos = sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES)[
            :per_student
        ]
        if photos:
            groups[folder.name] = photos
    return groups


def similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity of two unit-norm vectors."""
    return float(np.dot(a, b))


def embed_paired(photos: dict[str, list[Path]]) -> dict[str, list[tuple[np.ndarray, np.ndarray]]]:
    """Embed every photo under BOTH channel orders on the SAME image set.

    This is a **paired** comparison by construction: identical decoded pixels
    go through both orders, so the pair population is identical and a
    difference cannot be manufactured by different images surviving. An
    unpaired comparison is invalid here.
    """
    from app.core.domain.geometry import detect_and_embed

    out: dict[str, list[tuple[np.ndarray, np.ndarray]]] = {}
    for student, paths in photos.items():
        pairs: list[tuple[np.ndarray, np.ndarray]] = []
        for path in paths:
            try:
                bgr, _meta = decode(path.read_bytes())
            except Exception as exc:  # noqa: BLE001 - one bad file must not stop the run
                print(f"  skip {path.name}: {exc}", file=sys.stderr)
                continue
            rgb = np.ascontiguousarray(bgr[:, :, ::-1])
            correct = detect_and_embed(bgr)
            legacy = detect_and_embed(rgb)
            if correct is None or legacy is None:
                if (correct is None) != (legacy is None):
                    print(
                        f"  note: {student}/{path.name}: "
                        f"BGR={'NO FACE' if correct is None else 'ok'}, "
                        f"RGB={'NO FACE' if legacy is None else 'ok'}"
                    )
                continue
            pairs.append((correct, legacy))
        if pairs:
            out[student] = pairs
    return out


def report_pairs(
    pairs: dict[str, list[tuple[np.ndarray, np.ndarray]]],
    slot: int,
    order: str,
) -> dict[str, float]:
    """Compute separability and consistency for one channel order.

    Args:
        slot: 0 for the correct (BGR) embedding, 1 for the legacy (RGB) one.
    """
    same: list[float] = []
    different: list[float] = []
    spreads: list[float] = []

    students = sorted(pairs)
    for i, student_a in enumerate(students):
        vectors_a = [p[slot] for p in pairs[student_a]]
        for student_b in students[i + 1 :]:
            for va in vectors_a:
                for vb in [p[slot] for p in pairs[student_b]]:
                    different.append(similarity(va, vb))
        for j, va in enumerate(vectors_a):
            for vb in vectors_a[j + 1 :]:
                same.append(similarity(va, vb))
        if len(vectors_a) > 1:
            values = [
                similarity(vectors_a[a], vectors_a[b])
                for a in range(len(vectors_a))
                for b in range(a + 1, len(vectors_a))
            ]
            spreads.append(max(values) - min(values))

    mean_same = statistics.fmean(same) if same else float("nan")
    mean_diff = statistics.fmean(different) if different else float("nan")
    n_photos = sum(len(v) for v in pairs.values())

    print(f"\n--- {order} ---")
    print(f"  students / photos        : {len(students)} / {n_photos}")
    print(f"  same-person pairs        : {len(same)}")
    print(f"  different-person pairs   : {len(different)}")
    print(f"  same-person  mean        : {mean_same:.4f}")
    print(f"  same-person  p05         : {np.percentile(same, 5):.4f}")
    print(f"  different    mean        : {mean_diff:.4f}")
    print(f"  different    p95         : {np.percentile(different, 95):.4f}")
    print(f"  SEPARABILITY             : {mean_same - mean_diff:+.4f}   <-- higher is better")
    if spreads:
        print(f"  intra-student spread mean: {statistics.fmean(spreads):.4f}   <-- lower is better")

    return {
        "students": len(students),
        "photos": n_photos,
        "same_pairs": len(same),
        "diff_pairs": len(different),
        "same_mean": mean_same,
        "diff_mean": mean_diff,
        "separability": mean_same - mean_diff,
        "same_p05": float(np.percentile(same, 5)) if same else float("nan"),
        "diff_p95": float(np.percentile(different, 95)) if different else float("nan"),
        "intra_spread_mean": statistics.fmean(spreads) if spreads else float("nan"),
    }


def main(argv: list[str] | None = None) -> int:
    """Run the comparison and print the delta."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--photos", type=Path, default=Path("ENROLL_PHOTOS"))
    parser.add_argument("--per-student", type=int, default=8)
    parser.add_argument("--json", type=Path, help="write results as JSON")
    args = parser.parse_args(argv)

    photos = collect_photos(args.photos, args.per_student)
    total = sum(len(v) for v in photos.values())
    if len(photos) < 2 or total < 4:
        print(
            f"error: need at least 2 students and 4 photos, found "
            f"{len(photos)} students / {total} photos under {args.photos}",
            file=sys.stderr,
        )
        return 2

    registry = load_registry()
    print(f"date              : {datetime.now(UTC).date()}")
    print(f"model backend     : detector={registry.detector.name} embedder={registry.embedder.name}")
    print(f"embedding dim     : {registry.embedder.dimension}")
    print(f"image source      : {args.photos} ({len(photos)} students, {total} photos)")

    pairs = embed_paired(photos)
    if not pairs or sum(len(v) for v in pairs.values()) < 4:
        print("error: too few usable face pairs to compare", file=sys.stderr)
        return 1
    # Paired: identical images under both orders, so the pair populations match.
    results = {
        "rgb": report_pairs(pairs, slot=1, order="RGB (legacy, WRONG)"),
        "bgr": report_pairs(pairs, slot=0, order="BGR (fixed)"),
    }

    print("\n" + "=" * 62)
    print("VERDICT")
    print("=" * 62)
    legacy, fixed = results["rgb"], results["bgr"]
    delta = fixed["separability"] - legacy["separability"]
    print(f"  separability, legacy RGB  : {legacy['separability']:+.4f}")
    print(f"  separability, fixed  BGR  : {fixed['separability']:+.4f}")
    print(f"  delta                     : {delta:+.4f}")
    if delta > 0.01:
        print("  -> BGR is measurably better. The fix is justified by measurement.")
    elif delta < -0.01:
        print("  -> BGR is WORSE on this dataset. Investigate before trusting the fix.")
    else:
        print("  -> No measurable difference on this dataset.")
    print()
    print("  NOTE: the legacy pipeline used RGB *consistently* for both enrollment and")
    print("  inference, so matching still largely worked. The damage is (a) absolute")
    print("  embedding quality and (b) that any threshold calibrated on the RGB space is")
    print("  not comparable to published ArcFace/SFace figures.")

    if args.json:
        import json

        args.json.write_text(
            json.dumps({"date": str(datetime.now(UTC).date()), "results": results}, indent=2),
            encoding="utf-8",
        )
        print(f"\n  wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
