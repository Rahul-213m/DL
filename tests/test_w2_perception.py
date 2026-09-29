"""Perception pipeline tests.

Split into two groups:

* Pure tests, always run. Use a fake detector and embedder so CI needs no
  weights, no GPU and no network.
* ``@pytest.mark.requires_model`` tests, which run only where the OpenCV
  weights are present. They are marked, not skipped silently, so a CI job
  without weights reports "0 passed, N skipped" rather than pretending to have
  tested perception.
"""

from __future__ import annotations

import io
from datetime import UTC, datetime

import numpy as np
import pytest
from PIL import Image

from app.core.domain.types import BBox, FrameContext
from app.pipeline.perception import coverage_stats, process_frame_bytes

# ---------------------------------------------------------------------------
# Fakes: the whole point of the Detector/Embedder protocols (ADR 0004)
# ---------------------------------------------------------------------------


class FakeDetector:
    """Returns a fixed set of boxes, so tiling and NMS can be tested exactly."""

    name = "fake_detector"

    def __init__(self, boxes: list[tuple[BBox, float]]) -> None:
        self.boxes = boxes
        self.calls: list[tuple[int, int]] = []
        self._ready = False

    def warmup(self) -> None:
        """No weights to load."""
        self._ready = True

    def detect(self, image: np.ndarray) -> list[tuple[BBox, np.ndarray, float]]:
        """Return the configured boxes, offset into the tile."""
        height, width = image.shape[:2]
        self.calls.append((width, height))
        out = []
        for (x1, y1, x2, y2), score in self.boxes:
            # Landmarks must sit inside the box for alignment to be solvable.
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            half = max(2, min(x2 - x1, y2 - y1) // 4)
            landmarks = np.array(
                [
                    [cx - half, cy - half // 2],
                    [cx + half, cy - half // 2],
                    [cx, cy],
                    [cx - half, cy + half],
                    [cx + half, cy + half],
                ],
                dtype=np.float32,
            )
            out.append(((x1, y1, x2, y2), landmarks, score))
        del height
        return out

    def set_working_size(self, _size: int) -> None:
        """No-op for the fake."""


class FakeEmbedder:
    """Returns deterministic unit vectors keyed by box position."""

    name = "fake_embedder"
    dimension = 8

    def __init__(self) -> None:
        self.batches: list[int] = []

    def warmup(self) -> None:
        """No weights to load."""

    def embed(self, aligned_crop: np.ndarray) -> np.ndarray:
        """One vector per crop, derived from its mean so it is deterministic."""
        self.batches.append(1)
        value = float(aligned_crop.mean()) / 255.0
        vector = np.zeros(self.dimension, dtype=np.float32)
        vector[0] = value
        vector[1] = 1.0 - value
        norm = float(np.linalg.norm(vector))
        return (vector / norm).astype(np.float32)

    def embed_batch(self, aligned_crops: list[np.ndarray]) -> list[np.ndarray]:
        """Record the batch size so batching can be asserted."""
        self.batches.append(len(aligned_crops))
        return [self.embed(crop) for crop in aligned_crops]


@pytest.fixture
def fake_models(monkeypatch: pytest.MonkeyPatch) -> tuple[FakeDetector, FakeEmbedder]:
    """Install fakes as the process-wide registry."""
    from app.registry import loader

    detector = FakeDetector([((100, 100, 300, 300), 0.9)])
    embedder = FakeEmbedder()
    stub = loader.LoadedRegistry(loader.ModelRegistry(), detector, embedder)
    monkeypatch.setattr(loader, "_loaded", stub)
    return detector, embedder


def _png_bytes(array: np.ndarray) -> bytes:
    """Encode a numpy array to PNG bytes (lossless, so tests are deterministic)."""
    buffer = io.BytesIO()
    Image.fromarray(array).save(buffer, "PNG")
    return buffer.getvalue()


def _scene(width: int, height: int, seed: int = 0) -> np.ndarray:
    """A deterministic BGR test image, ``(height, width, 3)`` as numpy expects.

    Takes (width, height) because that is how a room is described, and converts
    to numpy's (height, width) ordering here so no test has to remember it.
    """
    rng = np.random.default_rng(seed)
    return rng.integers(0, 255, (height, width, 3), dtype=np.uint8)


def _context(**kwargs: object) -> FrameContext:
    base = {
        "frame_id": "frame-1",
        "session_id": 1,
        "tenant_id": "tenant-1",
        "captured_at": datetime(2026, 9, 29, 9, 0, tzinfo=UTC),
    }
    base.update(kwargs)
    return FrameContext(**base)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Pure pipeline tests
# ---------------------------------------------------------------------------


class TestPerceptionPipeline:
    """End-to-end on one frame, with fake models."""

    def test_a_clean_face_produces_an_embedding(self, fake_models: object) -> None:
        """The happy path."""
        result = process_frame_bytes(_png_bytes(_scene(400, 300)), _context())
        assert len(result.faces) == 1
        face = result.faces[0]
        assert face.embedding is not None
        assert face.embedding.shape == (8,)
        assert abs(float(np.linalg.norm(face.embedding)) - 1.0) < 1e-5
        assert face.aligned_crop, "evidence crop must be stored"

    def test_evidence_crop_is_the_aligned_crop(self, fake_models: object) -> None:
        """Audit 4.10: evidence must be what the model consumed.

        The stored bytes must decode to the same 112x112 image the embedder
        saw, not a raw bounding-box slice.
        """
        from app.core.domain.imageops import decode

        result = process_frame_bytes(_png_bytes(_scene(400, 300)), _context())
        evidence = result.faces[0].aligned_crop
        decoded, _meta = decode(evidence)
        assert decoded.shape == (112, 112, 3), (
            "stored evidence must be the aligned 112x112 crop, not a box slice"
        )

    def test_decode_metadata_is_propagated(self, fake_models: object) -> None:
        """Provenance of how the image was read reaches the result."""
        # _scene takes (width, height) = (320 wide, 240 tall).
        result = process_frame_bytes(_png_bytes(_scene(320, 240)), _context())
        assert result.metadata["width"] == 320
        assert result.metadata["height"] == 240
        assert result.metadata["channel_order"] == "BGR"

    def test_timings_are_recorded(self, fake_models: object) -> None:
        """Per-stage timings feed the benchmark and the trace."""
        result = process_frame_bytes(_png_bytes(_scene(400, 300)), _context())
        assert set(result.timings_ms) == {
            "decode_ms",
            "detect_ms",
            "quality_align_embed_ms",
        }
        assert all(value >= 0 for value in result.timings_ms.values())

    def test_low_score_face_is_rejected(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A detection below the score floor must not be embedded."""
        from app.registry import loader

        monkeypatch.setattr(
            loader,
            "_loaded",
            loader.LoadedRegistry(
                loader.ModelRegistry(), FakeDetector([((100, 100, 300, 300), 0.2)]), FakeEmbedder()
            ),
        )
        result = process_frame_bytes(_png_bytes(_scene(400, 300)), _context())
        assert result.faces == []
        assert any("low_detector_score" in reason for _obs, reason in result.rejected)

    def test_tiny_face_is_rejected_with_a_reason(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A 10px face cannot yield landmarks, and must say so."""
        from app.registry import loader

        monkeypatch.setattr(
            loader,
            "_loaded",
            loader.LoadedRegistry(
                loader.ModelRegistry(), FakeDetector([((10, 10, 20, 20), 0.9)]), FakeEmbedder()
            ),
        )
        result = process_frame_bytes(_png_bytes(_scene(400, 300)), _context())
        assert result.faces == []
        assert result.rejected, "a rejection must carry a reason, not vanish"

    def test_small_but_usable_face_requests_recapture(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A 40px face is matched but must trigger a zoom pass."""
        from app.registry import loader

        monkeypatch.setattr(
            loader,
            "_loaded",
            loader.LoadedRegistry(
                loader.ModelRegistry(), FakeDetector([((100, 100, 140, 140), 0.9)]), FakeEmbedder()
            ),
        )
        result = process_frame_bytes(_png_bytes(_scene(400, 300)), _context())
        assert len(result.faces) == 1
        assert result.faces[0].needs_recapture
        assert result.recapture_regions, "the scan planner needs the region to revisit"
        assert not result.faces[0].can_auto_confirm

    def test_large_sharp_face_does_not_request_recapture(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A 200px face is above the quality bar."""
        from app.registry import loader

        monkeypatch.setattr(
            loader,
            "_loaded",
            loader.LoadedRegistry(
                loader.ModelRegistry(), FakeDetector([((50, 50, 250, 250), 0.95)]), FakeEmbedder()
            ),
        )
        result = process_frame_bytes(_png_bytes(_scene(400, 300)), _context())
        assert len(result.faces) == 1
        assert not result.faces[0].needs_recapture

    def test_a_frame_with_one_broken_face_still_others(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """One unusable face must not fail the whole frame."""
        from app.registry import loader

        class HalfBrokenEmbedder(FakeEmbedder):
            """Fails on the second embed call only."""

            def __init__(self) -> None:
                super().__init__()
                self.calls = 0

            def embed(self, aligned_crop: np.ndarray) -> np.ndarray:
                """Count separately from batches; super() also appends."""
                self.calls += 1
                if self.calls == 2:
                    raise RuntimeError("simulated ONNX failure")
                return super().embed(aligned_crop)

        monkeypatch.setattr(
            loader,
            "_loaded",
            loader.LoadedRegistry(
                loader.ModelRegistry(),
                FakeDetector([((20, 20, 220, 220), 0.9), ((300, 20, 500, 220), 0.9)]),
                HalfBrokenEmbedder(),
            ),
        )
        result = process_frame_bytes(_png_bytes(_scene(600, 400)), _context())
        assert len(result.faces) == 1, "the surviving face must still be reported"
        assert any("embed_failed" in reason for _obs, reason in result.rejected)

    def test_tiling_bounds_the_detector_calls(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A huge frame must not create unbounded inference calls."""
        from app.registry import loader

        detector = FakeDetector([((10, 10, 60, 60), 0.9)])
        monkeypatch.setattr(
            loader, "_loaded", loader.LoadedRegistry(loader.ModelRegistry(), detector, FakeEmbedder())
        )
        # 6000x4500 at a 1600 target wants 4x3=12 tiles plus the full frame;
        # the cap must hold it at 16 total.
        process_frame_bytes(_png_bytes(_scene(6000, 4500)), _context())
        assert len(detector.calls) <= 16

    def test_oversized_frame_is_rejected_before_inference(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """The decompression-bomb guard runs before the detector is touched."""
        from app.core.domain.imageops import ImageTooLargeError
        from app.registry import loader

        detector = FakeDetector([((10, 10, 60, 60), 0.9)])
        monkeypatch.setattr(
            loader, "_loaded", loader.LoadedRegistry(loader.ModelRegistry(), detector, FakeEmbedder())
        )
        # 8000x6000 = 48,000,000 px, over the 36,000,000 limit.
        with pytest.raises(ImageTooLargeError):
            process_frame_bytes(_png_bytes(_scene(8000, 6000)), _context())
        assert detector.calls == [], "no inference may happen on a rejected image"

    def test_no_tiling_for_a_small_frame(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """A sub-threshold frame needs exactly one pass."""
        from app.registry import loader

        detector = FakeDetector([((10, 10, 60, 60), 0.9)])
        monkeypatch.setattr(
            loader, "_loaded", loader.LoadedRegistry(loader.ModelRegistry(), detector, FakeEmbedder())
        )
        process_frame_bytes(_png_bytes(_scene(640, 480)), _context())
        assert len(detector.calls) == 1

    def test_corrupt_bytes_raise_rather_than_return_empty(self, fake_models: object) -> None:
        """A corrupt upload is a client error, not a silent empty frame."""
        from app.core.domain.imageops import ImageDecodeError

        with pytest.raises(ImageDecodeError):
            process_frame_bytes(b"this is not an image", _context())

    def test_evidence_can_be_skipped_for_detection_only_passes(self, fake_models: object) -> None:
        """A cheap wide pass should not pay for JPEG encoding."""
        result = process_frame_bytes(_png_bytes(_scene(400, 300)), _context(), store_evidence_crops=False)
        assert len(result.faces) == 1
        assert result.faces[0].aligned_crop == b""


class TestCoverageStats:
    """The coverage acceptance metric needs the roster to mean anything."""

    def test_coverage_is_optional_without_an_expected_count(self) -> None:
        """Without a roster there is nothing to compute coverage against."""
        from app.pipeline.perception import FrameResult

        stats = coverage_stats(FrameResult(context=_context(), image=np.zeros((4, 4, 3), np.uint8)))
        assert "coverage" not in stats
        assert stats["faces_usable"] == 0.0

    def test_coverage_is_capped_at_one(self) -> None:
        """More faces than expected students must not report >100%."""
        from app.core.domain.quality import Quality, QualityReport
        from app.core.domain.types import FaceObservation
        from app.pipeline.perception import (
            DetectedFaceResult,
            FrameResult,
        )

        faces = [
            DetectedFaceResult(
                observation=FaceObservation((0, 0, 100, 100), (), 0.9),
                embedding=np.zeros(4, np.float32),
                aligned_crop=b"",
                quality=QualityReport(Quality.GOOD),
            )
            for _ in range(5)
        ]
        result = FrameResult(context=_context(), image=np.zeros((4, 4, 3), np.uint8), faces=faces)
        assert coverage_stats(result, expected_students=3)["coverage"] == 1.0


# ---------------------------------------------------------------------------
# Real-model tests
# ---------------------------------------------------------------------------


@pytest.mark.requires_model
class TestPerceptionWithRealModels:
    """Exercises the actual OpenCV backend. Skipped where weights are absent."""

    def test_detects_a_face_in_a_real_portrait(self) -> None:
        """The permissive baseline must actually work end to end."""
        from pathlib import Path

        photos = sorted(Path("ENROLL_PHOTOS").glob("*/*.jpg"))
        if not photos:
            pytest.skip("no enrollment photos available")

        from app.core.domain.imageops import decode

        data = photos[0].read_bytes()
        result = process_frame_bytes(data, _context())
        assert result.faces, f"no face found in {photos[0]}"
        face = result.faces[0]
        assert face.embedding is not None
        assert face.embedding.shape == (128,), "SFace produces 128-d embeddings"
        assert abs(float(np.linalg.norm(face.embedding)) - 1.0) < 1e-4
        del decode

    def test_channel_order_is_bgr_throughout(self) -> None:
        """The pipeline must never hand RGB to a BGR model."""
        from pathlib import Path

        from app.core.domain.imageops import decode

        photos = sorted(Path("ENROLL_PHOTOS").glob("*/*.jpg"))
        if not photos:
            pytest.skip("no enrollment photos available")
        bgr, meta = decode(photos[0].read_bytes())
        assert meta["channel_order"] == "BGR"
        result = process_frame_bytes(photos[0].read_bytes(), _context())
        assert np.array_equal(result.image, bgr), "the pipeline must reuse the decoded array"
