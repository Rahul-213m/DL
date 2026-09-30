"""Benchmark helpers report stable aggregates and only explicit image inputs."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts import benchmark_pipeline
from scripts.benchmark_pipeline import image_files, percentile, summarize


def test_percentile_uses_nearest_rank_values() -> None:
    assert percentile([10.0, 1.0, 5.0, 2.0], 0.50) == 2.0
    assert percentile([10.0, 1.0, 5.0, 2.0], 0.95) == 10.0


def test_image_file_discovery_is_explicit_and_deterministic(tmp_path: Path) -> None:
    (tmp_path / "b.jpg").write_bytes(b"not decoded by discovery")
    (tmp_path / "a.png").write_bytes(b"not decoded by discovery")
    (tmp_path / "notes.txt").write_text("not an image")

    assert [path.name for path in image_files([tmp_path])] == ["a.png", "b.jpg"]


def test_summary_exposes_aggregate_latency_and_coverage_only() -> None:
    report = summarize(
        [
            {
                "wall_ms": 20.0,
                "timings_ms": {"decode_ms": 5.0, "detect_ms": 10.0},
                "faces": 2,
                "rejected": 1,
                "recapture_regions": 1,
            },
            {
                "wall_ms": 30.0,
                "timings_ms": {"decode_ms": 7.0, "detect_ms": 15.0},
                "faces": 3,
                "rejected": 0,
                "recapture_regions": 0,
            },
        ],
        0.05,
    )

    assert report["wall_latency_ms"] == {"p50": 20.0, "p95": 30.0}
    assert report["coverage"] == {
        "detected_faces": 5,
        "rejected_faces": 1,
        "recapture_regions": 1,
    }
    assert all("path" not in key for key in report)


def test_percentile_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="no values"):
        percentile([], 0.5)


def test_run_throughput_excludes_warmup_time(monkeypatch, tmp_path: Path) -> None:
    image = tmp_path / "frame.jpg"
    image.write_bytes(b"benchmark input")
    clock = [0.0]

    def fake_process(*_args, **_kwargs):
        clock[0] += 100.0 if clock[0] == 0.0 else 2.0
        return SimpleNamespace(timings_ms={"detect_ms": 1.0}, faces=[], rejected=[], recapture_regions=[])

    monkeypatch.setattr(benchmark_pipeline, "process_frame_bytes", fake_process)
    monkeypatch.setattr(benchmark_pipeline.time, "perf_counter", lambda: clock[0])

    report = benchmark_pipeline.run_benchmark([image], runs=1, warmup=1)

    assert report["elapsed_seconds"] == 2.0
    assert report["throughput_frames_per_second"] == 0.5
