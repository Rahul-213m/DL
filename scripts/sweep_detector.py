#!/usr/bin/env python3
"""Sweep the YuNet detector operating point on real photographs.

Answers a question that cannot be answered from documentation: at what
detector working size and score threshold does the permissive baseline stop
producing garbage on this deployment's actual images?

The labels used here are weak, and the script says so: the enrollment photos
in ENROLL_PHOTOS/ are single-person portraits, so the one large centred face
is a true positive and everything else is a false positive. That is a good
proxy for precision on the enrollment path and a poor proxy for recall on a
dense classroom. The classroom recall question needs a labelled classroom set
(protocol: docs/data_collection_protocol.md) and is UNVERIFIED until then.

Usage:
    python scripts/sweep_detector.py
    python scripts/sweep_detector.py --photos ENROLL_PHOTOS --limit 24 --json out.json
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.domain.geometry import box_area, iou
from app.core.domain.imageops import decode
from app.registry.backends.opencv_yunet_sface import YuNetDetector

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}


def load_images(root: Path, limit: int) -> list[tuple[str, np.ndarray]]:
    """Load up to ``limit`` single-person portraits."""
    images: list[tuple[str, np.ndarray]] = []
    for folder in sorted(p for p in root.iterdir() if p.is_dir()):
        for path in sorted(folder.iterdir()):
            if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            try:
                bgr, _meta = decode(path.read_bytes())
            except Exception as exc:  # noqa: BLE001 - a bad file must not stop the sweep
                print(f"  skip {path.name}: {exc}", file=sys.stderr)
                continue
            images.append((f"{folder.name}/{path.name}", bgr))
            if len(images) >= limit:
                return images
    return images


def centre_box(image: np.ndarray) -> tuple[int, int, int, int]:
    """The central third of the frame, used as a loose 'true face' region."""
    h, w = image.shape[:2]
    return (w // 3, h // 3, 2 * w // 3, 2 * h // 3)


def evaluate(
    detector: YuNetDetector,
    images: list[tuple[str, np.ndarray]],
) -> dict[str, float]:
    """Run the detector over the set and score precision/recall/speed."""
    detected = 0
    false_positives = 0
    true_positives = 0
    latencies: list[float] = []
    top_face_px: list[int] = []

    for _name, image in images:
        start = time.perf_counter()
        faces = detector.detect(image)
        latencies.append(time.perf_counter() - start)

        detected += len(faces)
        if faces:
            top_face_px.append(max(box_area(f[0]) for f in faces) ** 0.5)
        if any(iou(f[0], centre_box(image)) > 0.05 for f in faces):
            true_positives += 1
        if len(faces) > 1:
            false_positives += len(faces) - 1

    total = len(images) or 1
    return {
        "images": total,
        "detections_per_image": detected / total,
        "false_positives_per_image": false_positives / total,
        "recall": true_positives / total,
        "precision": (true_positives / detected) if detected else 0.0,
        "median_latency_ms": statistics.median(latencies) * 1000.0,
        "median_face_side_px": float(np.median(top_face_px)) if top_face_px else 0.0,
    }


def main(argv: list[str] | None = None) -> int:
    """Sweep and print a table."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--photos", type=Path, default=Path("ENROLL_PHOTOS"))
    parser.add_argument("--limit", type=int, default=24)
    parser.add_argument("--json", type=Path)
    args = parser.parse_args(argv)

    images = load_images(args.photos, args.limit)
    if len(images) < 4:
        print(f"error: need at least 4 usable images, got {len(images)}", file=sys.stderr)
        return 2

    print(f"date            : {datetime.now(UTC).date()}")
    print(f"images          : {len(images)} single-person portraits from {args.photos}")
    print(f"image size      : {images[0][1].shape[1]}x{images[0][1].shape[0]}")
    print("label           : 1 large centred face = TP, everything else = FP")
    print()
    header = (
        f"{'working':>8} {'thresh':>7} {'FP/img':>7} {'recall':>7} {'prec':>6} {'ms/img':>7} {'face px':>8}"
    )
    print(header)
    print("-" * len(header))

    results: dict[str, dict[str, float]] = {}
    for size in (320, 480, 640, 960, 1280):
        for threshold in (0.6, 0.7, 0.8, 0.9):
            detector = YuNetDetector(working_size=size, score_threshold=threshold)
            row = evaluate(detector, images)
            results[f"{size}@{threshold}"] = row
            print(
                f"{size:>8} {threshold:>7.2f} {row['false_positives_per_image']:>7.2f} "
                f"{row['recall']:>7.2f} {row['precision']:>6.2f} "
                f"{row['median_latency_ms']:>7.1f} {row['median_face_side_px']:>8.0f}"
            )

    print()
    print("=" * 62)
    print("READING THIS TABLE")
    print("=" * 62)
    print("  FP/img    lower is better. A classroom frame legitimately contains")
    print("            ~300 faces, so a small FP count is not fatal for a SCAN;")
    print("            it IS fatal for ENROLLMENT, where a second face means the")
    print("            wrong person gets added to a gallery.")
    print("  recall    fraction of portraits where a face was found at all.")
    print("  ms/img    CPU only, on this laptop. NOT the production number --")
    print("            see docs/benchmarks.md for the AWS GPU protocol.")
    print()
    print("  CAVEAT: recall here is recall on PORTRAITS, not on a dense")
    print("  classroom. Back-row coverage is the question that actually matters")
    print("  and it is UNVERIFIED until a labelled classroom set exists.")

    if args.json:
        args.json.write_text(
            json.dumps(
                {"date": str(datetime.now(UTC).date()), "n_images": len(images), "sweep": results},
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"\n  wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
