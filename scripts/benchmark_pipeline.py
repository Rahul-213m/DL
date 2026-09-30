#!/usr/bin/env python3
"""Measure end-to-end perception latency on explicitly selected image files.

This benchmark runs the configured detector and embedder without persisting
frames, crops, embeddings, or source paths. Use only data approved for this
purpose; the JSON output contains aggregate timing and coverage measurements.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import settings
from app.core.domain.types import FrameContext
from app.pipeline.perception import process_frame_bytes

IMAGE_EXTENSIONS = {".bmp", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}


def image_files(inputs: list[Path]) -> list[Path]:
    """Expand explicit files/directories into a stable list of image paths."""
    paths: set[Path] = set()
    for source in inputs:
        if source.is_file() and source.suffix.lower() in IMAGE_EXTENSIONS:
            paths.add(source.resolve())
        elif source.is_dir():
            paths.update(
                path.resolve()
                for path in source.rglob("*")
                if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
            )
        else:
            raise ValueError(f"not an image file or directory: {source}")
    if not paths:
        raise ValueError("no supported image files found")
    return sorted(paths)


def percentile(values: list[float], fraction: float) -> float:
    """Return a nearest-rank percentile without requiring NumPy statistics."""
    if not values:
        raise ValueError("cannot compute a percentile from no values")
    if not 0.0 <= fraction <= 1.0:
        raise ValueError("fraction must be in [0, 1]")
    ordered = sorted(values)
    index = max(0, math.ceil(len(ordered) * fraction) - 1)
    return ordered[index]


def summarize(samples: list[dict[str, Any]], elapsed_seconds: float) -> dict[str, Any]:
    """Aggregate per-run timings and coverage without exposing image paths."""
    timing_keys = sorted({key for row in samples for key in row["timings_ms"]})
    timings = {
        key: {
            "p50_ms": percentile([row["timings_ms"][key] for row in samples], 0.50),
            "p95_ms": percentile([row["timings_ms"][key] for row in samples], 0.95),
        }
        for key in timing_keys
    }
    wall_times = [row["wall_ms"] for row in samples]
    return {
        "status": "complete",
        "runs": len(samples),
        "elapsed_seconds": elapsed_seconds,
        "throughput_frames_per_second": len(samples) / elapsed_seconds if elapsed_seconds > 0 else 0.0,
        "wall_latency_ms": {
            "p50": percentile(wall_times, 0.50),
            "p95": percentile(wall_times, 0.95),
        },
        "stage_latency_ms": timings,
        "coverage": {
            "detected_faces": sum(row["faces"] for row in samples),
            "rejected_faces": sum(row["rejected"] for row in samples),
            "recapture_regions": sum(row["recapture_regions"] for row in samples),
        },
    }


def run_benchmark(paths: list[Path], *, runs: int, warmup: int) -> dict[str, Any]:
    """Execute the configured pipeline and return privacy-minimised metrics."""
    if runs < 1 or warmup < 0:
        raise ValueError("runs must be >= 1 and warmup must be >= 0")

    samples: list[dict[str, Any]] = []
    failures = 0
    measurement_started: float | None = None
    total_iterations = warmup + runs
    for iteration in range(total_iterations):
        warmup_run = iteration < warmup
        if not warmup_run and measurement_started is None:
            measurement_started = time.perf_counter()
        for sample_index, path in enumerate(paths):
            data = path.read_bytes()
            context = FrameContext(
                frame_id=f"benchmark-{iteration}-{sample_index}",
                session_id=0,
                tenant_id="benchmark",
                captured_at=datetime.now(UTC),
            )
            wall_started = time.perf_counter()
            try:
                result = process_frame_bytes(data, context, store_evidence_crops=False)
            except Exception as exc:  # noqa: BLE001 - report failed samples, continue the run
                failures += 1
                if not warmup_run:
                    samples.append(
                        {
                            "wall_ms": (time.perf_counter() - wall_started) * 1000.0,
                            "timings_ms": {},
                            "faces": 0,
                            "rejected": 0,
                            "recapture_regions": 0,
                            "failed": type(exc).__name__,
                        }
                    )
                continue

            if not warmup_run:
                samples.append(
                    {
                        "wall_ms": (time.perf_counter() - wall_started) * 1000.0,
                        "timings_ms": result.timings_ms,
                        "faces": len(result.faces),
                        "rejected": len(result.rejected),
                        "recapture_regions": len(result.recapture_regions),
                    }
                )

    elapsed = time.perf_counter() - measurement_started if measurement_started is not None else 0.0
    successful = [row for row in samples if "failed" not in row]
    summary = (
        summarize(successful, elapsed)
        if successful
        else {
            "status": "failed",
            "runs": 0,
            "elapsed_seconds": elapsed,
            "throughput_frames_per_second": 0.0,
            "wall_latency_ms": None,
            "stage_latency_ms": {},
            "coverage": {"detected_faces": 0, "rejected_faces": 0, "recapture_regions": 0},
        }
    )
    summary.update(
        {
            "requested_runs": runs * len(paths),
            "warmup_runs": warmup * len(paths),
            "failed_runs": failures,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "detector_backend": settings.detector_backend,
            "embedder_backend": settings.embedder_backend,
            "execution_providers": settings.provider_list,
        }
    )
    if failures:
        summary["status"] = "partial" if successful else "failed"
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="Image files and/or directories")
    parser.add_argument("--runs", type=int, default=3, help="Measured repetitions per image")
    parser.add_argument("--warmup", type=int, default=1, help="Discarded repetitions per image")
    parser.add_argument("--json", type=Path, help="Write aggregate metrics to this path")
    args = parser.parse_args(argv)

    try:
        report = run_benchmark(image_files(args.inputs), runs=args.runs, warmup=args.warmup)
    except (OSError, ValueError) as exc:
        print(f"benchmark error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0 if report["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
