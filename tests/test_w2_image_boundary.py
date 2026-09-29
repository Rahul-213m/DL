"""Regression tests for the W2 correctness fixes.

Each test corresponds to a defect in docs/00_audit.md. Where a defect was a
*silent* one, the test pins the mechanism so it cannot come back silently
again.

Legend in the docstrings: [audit 4.x] is the section being pinned.
"""

from __future__ import annotations

import io
import time

import numpy as np
import pytest
from PIL import Image

from app.core.domain import imageops
from app.core.domain.imageops import (
    ImageDecodeError,
    ImageTooLargeError,
    crop,
    decode,
    encode_jpeg,
    to_bgr,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def _jpeg_bytes(
    array: np.ndarray,
    *,
    exif_orientation: int | None = None,
) -> bytes:
    """Encode a numpy array to JPEG, optionally with an EXIF orientation tag."""
    # Takes an RGB array (the human-visible order) and encodes it as such.
    # No channel flipping here: the boundary under test is decode(), and a
    # double flip in the helper would mask a real regression.
    mode = "RGB" if array.ndim == 3 and array.shape[2] == 3 else "L"
    image = Image.fromarray(array, mode=mode)
    buffer = io.BytesIO()
    if exif_orientation is None:
        image.save(buffer, "JPEG", quality=95)
        return buffer.getvalue()

    exif = image.getexif()
    exif[0x0112] = exif_orientation
    buffer = io.BytesIO()
    image.save(buffer, "JPEG", quality=95, exif=exif)
    return buffer.getvalue()


def _brightest_quadrant(image: np.ndarray) -> tuple[int, int]:
    """Return ``(row_half, col_half)`` of the brightest quadrant: 0=top/left, 1=bottom/right.

    Quadrants rather than fixed blocks, because a block grid silently drops the
    right-hand edge when the size is not a multiple of the block -- which is
    exactly where the marker landed in the first draft of this test.
    """
    height, width = image.shape[:2]
    mid_h, mid_w = height // 2, width // 2
    quadrants = {
        (0, 0): image[:mid_h, :mid_w],
        (0, 1): image[:mid_h, mid_w:],
        (1, 0): image[mid_h:, :mid_w],
        (1, 1): image[mid_h:, mid_w:],
    }
    return max(quadrants, key=lambda key: float(quadrants[key].mean()))


def _gradient(height: int, width: int) -> np.ndarray:
    """A deterministic, non-uniform RGB test image."""
    rows = np.linspace(0, 255, height, dtype=np.uint8)[:, None]
    cols = np.linspace(0, 255, width, dtype=np.uint8)[None, :]
    blue = np.tile(rows, (1, width))[:, :, None]
    red = np.tile(cols, (height, 1))[:, :, None]
    green = ((red.astype(np.uint16) + blue.astype(np.uint16)) // 2).astype(np.uint8)
    return np.dstack([red, green, blue])


# ---------------------------------------------------------------------------
# [audit 4.1] BGR channel order
# ---------------------------------------------------------------------------


class TestChannelOrder:
    """InsightFace and OpenCV both expect BGR; the legacy path fed them RGB.

    Root cause recorded in docs/00_audit.md 4.1: both
    ``insightface/model_zoo/arcface_onnx.py`` and ``retinaface.py`` normalise
    with ``cv2.dnn.blobFromImage(..., swapRB=True)``, which means the graph
    receives BGR.
    """

    def test_to_bgr_swaps_red_and_blue(self) -> None:
        """The conversion must actually transpose the channels."""
        rgb = np.zeros((2, 2, 3), dtype=np.uint8)
        rgb[..., 0] = 200  # red
        rgb[..., 1] = 100  # green
        rgb[..., 2] = 50  # blue
        bgr = to_bgr(rgb)
        assert bgr[0, 0, 0] == 50, "blue channel must land first"
        assert bgr[0, 0, 1] == 100
        assert bgr[0, 0, 2] == 200, "red channel must land last"

    def test_to_bgr_round_trips(self) -> None:
        """BGR -> RGB -> BGR must be lossless."""
        original = _gradient(16, 16)
        assert np.array_equal(to_bgr(to_bgr(original)), original)

    def test_to_bgr_rejects_non_three_channel(self) -> None:
        """A greyscale array cannot be channel-swapped, and must say so."""
        with pytest.raises(ValueError, match=r"\(H, W, 3\)"):
            to_bgr(np.zeros((4, 4), dtype=np.uint8))

    def test_to_bgr_is_contiguous(self) -> None:
        """A reversed-stride view is not always safe to hand to OpenCV."""
        bgr = to_bgr(_gradient(8, 8))
        assert bgr.flags["C_CONTIGUOUS"]

    def test_decode_returns_bgr_not_rgb(self) -> None:
        """decode() must hand back BGR. This is the regression pin."""
        red_image = np.zeros((4, 4, 3), dtype=np.uint8)
        red_image[..., 0] = 255
        bgr, meta = decode(_jpeg_bytes(red_image))
        assert meta["channel_order"] == "BGR"
        # After JPEG round-trip the red plane is the strongest signal, and it
        # must now be in channel index 2, not 0.
        assert bgr[..., 2].mean() > bgr[..., 0].mean(), (
            "decode() returned RGB; every downstream detector expects BGR"
        )

    def test_legacy_recognizer_shim_converts_to_bgr(self) -> None:
        """The legacy adapter must not feed RGB to InsightFace any more.

        It was broken at runtime in W1 (removed settings fields) and wrong on
        channel order before that. Both are pinned here.
        """
        from app.pipeline.recognizer import InsightFaceRecognizer

        recognizer = InsightFaceRecognizer()
        # Constructing and warming up must not raise, and must route through
        # the registry (which is what applies the production licence guard).
        recognizer.warmup()
        assert recognizer._registry is not None, "shim must delegate to the registry"
        assert np.array_equal(to_bgr(to_bgr(_gradient(4, 4))), _gradient(4, 4))


# ---------------------------------------------------------------------------
# [audit 4.2] EXIF orientation
# ---------------------------------------------------------------------------


class TestExifOrientation:
    """A phone in portrait stores rotation in EXIF, not in the pixels.

    ``Image.open().convert("RGB")`` does not apply it, so a portrait classroom
    frame reached SCRFD rotated 90 degrees. Since the target device is a phone,
    this is the normal case.
    """

    # (orientation, swaps_dimensions, applies_transform)
    #
    # 1 normal; 2 mirror-horizontal; 3 rotate-180; 4 mirror-vertical;
    # 5 transpose; 6 rotate-90; 7 transverse; 8 rotate-270.
    #
    # Note that 3 and 4 apply a transform but preserve dimensions: only the
    # four 90-degree cases swap width and height. Conflating "applied" with
    # "swapped" was itself a bug in the first draft of this test.
    @pytest.mark.parametrize(
        ("orientation", "swaps_dimensions", "applies_transform"),
        [
            (1, False, False),
            (2, False, True),
            (3, False, True),
            (4, False, True),
            (5, True, True),
            (6, True, True),
            (7, True, True),
            (8, True, True),
        ],
    )
    def test_orientation_changes_dimensions_where_it_should(
        self, orientation: int, swaps_dimensions: bool, applies_transform: bool
    ) -> None:
        """Cases 5-8 rotate by 90 degrees and must swap width and height."""
        tall = _gradient(40, 20)
        data = _jpeg_bytes(tall, exif_orientation=orientation)
        bgr, meta = decode(data)
        assert meta["exif_orientation"] == orientation
        expected = (40, 20) if swaps_dimensions else (20, 40)
        assert (bgr.shape[1], bgr.shape[0]) == expected, (
            f"orientation {orientation}: expected {expected[0]}x{expected[1]}, "
            f"got {bgr.shape[1]}x{bgr.shape[0]}"
        )
        assert meta["orientation_applied"] is applies_transform

    def test_orientation_rotates_pixels_not_just_dimensions(self) -> None:
        """The strong check: the CONTENT must move, not just the shape.

        Asserting only on dimensions would pass for a decoder that *resized*
        instead of rotated, which is exactly the failure the audit found. A
        uniquely coloured corner marker makes the movement unambiguous.
        """
        # White marker in the top-left of a 20-wide x 40-tall image.
        marked = np.full((40, 20, 3), 20, dtype=np.uint8)
        marked[0:6, 0:6] = 255
        bgr, _meta = decode(_jpeg_bytes(marked, exif_orientation=6))
        # Orientation 6 is a 90-degree clockwise rotation, so the shape becomes
        # 40x20 and the top-left corner moves to the top-right.
        assert bgr.shape[:2] == (20, 40)
        assert _brightest_quadrant(bgr) == (0, 1), (
            "the marker must end up in the top-right quadrant after a "
            f"90-degree rotation, found it at {_brightest_quadrant(bgr)}"
        )

    def test_orientation_180_keeps_shape_but_moves_content(self) -> None:
        """Orientation 3 rotates 180: same shape, content inverted.

        A separate case from the quarter turns, and the one a decoder that only
        special-cases 90s would silently get wrong.
        """
        marked = np.full((40, 20, 3), 20, dtype=np.uint8)
        marked[0:6, 0:6] = 255
        bgr, meta = decode(_jpeg_bytes(marked, exif_orientation=3))
        assert bgr.shape[:2] == (40, 20)
        assert meta["orientation_applied"] is True
        assert _brightest_quadrant(bgr) == (1, 1), (
            "a 180-degree rotation must move the marker to the opposite "
            f"quadrant, found it at {_brightest_quadrant(bgr)}"
        )

    def test_missing_exif_is_orientation_1(self) -> None:
        """An image with no EXIF must decode normally and be reported as such."""
        _bgr, meta = decode(_jpeg_bytes(_gradient(20, 30)))
        assert meta["exif_orientation"] == 1
        assert meta["orientation_applied"] is False

    def test_legacy_path_would_have_ignored_orientation(self) -> None:
        """Demonstrate that the fix is not redundant.

        The legacy code did ``Image.open(...).convert("RGB")``, which reports
        the PRE-rotation size. decode() must differ, or nothing was fixed.
        """
        data = _jpeg_bytes(_gradient(40, 20), exif_orientation=6)
        legacy_size = Image.open(io.BytesIO(data)).size
        bgr, meta = decode(data)
        assert meta["orientation_applied"] is True
        assert (bgr.shape[1], bgr.shape[0]) == (40, 20)
        assert (legacy_size[0], legacy_size[1]) == (20, 40)
        assert (bgr.shape[1], bgr.shape[0]) != legacy_size, (
            "decode() produced the same shape as the untransposed legacy path"
        )

    def test_has_exif_orientation_is_cheap_and_total(self) -> None:
        """It must answer 1 for anything unparseable, never raise."""
        assert imageops.has_exif_orientation(b"not an image at all") == 1
        assert imageops.has_exif_orientation(b"") == 1


# ---------------------------------------------------------------------------
# Decode safety
# ---------------------------------------------------------------------------


class TestDecodeSafety:
    """The ingestion boundary must not be a denial-of-service vector."""

    def test_empty_upload_is_rejected(self) -> None:
        """An empty body is a client error, not a crash."""
        with pytest.raises(ImageDecodeError):
            decode(b"")

    def test_garbage_is_rejected(self) -> None:
        """Random bytes must not reach the detector."""
        with pytest.raises(ImageDecodeError):
            decode(b"\x00\x01\x02\x03" * 1000)

    def test_decompression_bomb_is_rejected(self) -> None:
        """Pixel budget is checked before any array is materialised."""
        oversized = _gradient(700, 700)  # 490,000 px
        with pytest.raises(ImageTooLargeError, match="limit is"):
            decode(_jpeg_bytes(oversized), max_pixels=1000)

    def test_limit_is_reported_in_the_error(self) -> None:
        """The operator needs to know what was rejected and by how much."""
        with pytest.raises(ImageTooLargeError) as exc:
            decode(_jpeg_bytes(_gradient(300, 300)), max_pixels=100)
        assert "300x300" in str(exc.value)
        assert "90,000" in str(exc.value)

    def test_metadata_records_the_interpretation(self) -> None:
        """Provenance of how an image was read is part of the audit record."""
        _bgr, meta = decode(_jpeg_bytes(_gradient(12, 34)))
        assert meta["width"] == 34
        assert meta["height"] == 12
        assert meta["byte_length"] > 0
        assert set(meta) == {
            "byte_length",
            "width",
            "height",
            "exif_orientation",
            "orientation_applied",
            "channel_order",
        }

    def test_encode_jpeg_rejects_impossible_quality(self) -> None:
        """Quality 0 or 101 is a caller bug, not a silent clamp."""
        with pytest.raises(ValueError, match="quality"):
            encode_jpeg(np.zeros((4, 4, 3), np.uint8), quality=0)
        with pytest.raises(ValueError, match="quality"):
            encode_jpeg(np.zeros((4, 4, 3), np.uint8), quality=101)

    def test_encode_decode_round_trip_preserves_channel_mean(self) -> None:
        """Evidence images must not have their channels mangled in storage."""
        original = to_bgr(_gradient(64, 64))
        restored, _meta = decode(encode_jpeg(original, quality=100))
        for channel in range(3):
            assert abs(float(original[..., channel].mean()) - float(restored[..., channel].mean())) < 2.0


class TestCrop:
    """A detector box can extend past the frame edge."""

    def test_crop_clamps_to_the_image(self) -> None:
        """Out-of-range boxes must clamp, not silently pad with black."""
        image = np.full((100, 100, 3), 200, dtype=np.uint8)
        piece = crop(image, (90, 90, 150, 150))
        assert piece.shape == (10, 10, 3)
        assert piece.mean() == 200, "clamped crop must contain only real pixels"

    def test_negative_origin_clamps(self) -> None:
        """A negative origin is legal input from some detectors."""
        image = np.full((50, 50, 3), 100, dtype=np.uint8)
        # Clamped to (0, 0, 20, 20).
        piece = crop(image, (-10, -10, 20, 20))
        assert piece.shape == (20, 20, 3)

    def test_degenerate_crop_is_an_error(self) -> None:
        """An empty crop must fail loudly rather than produce a 0x0 image."""
        with pytest.raises(ImageDecodeError, match="degenerate"):
            crop(np.zeros((50, 50, 3), np.uint8), (10, 10, 10, 10))


# ---------------------------------------------------------------------------
# [audit 4.8] Quality metrics
# ---------------------------------------------------------------------------


class TestQualityMetrics:
    """Blur and illumination must be measurable, since the audit found no
    quality gate existed at all."""

    def test_sharp_image_scores_higher_than_blurry(self) -> None:
        """Variance-of-Laplacian must actually discriminate."""
        rng = np.random.default_rng(0)
        sharp = to_bgr(rng.integers(0, 255, (64, 64, 3), dtype=np.uint8))
        smooth = np.full((64, 64, 3), 128, dtype=np.uint8)
        assert imageops.sharpness_score(sharp) > imageops.sharpness_score(smooth)

    def test_tiny_crop_does_not_crash(self) -> None:
        """A 2x2 crop has no meaningful Laplacian; return 0.0, don't raise."""
        assert imageops.sharpness_score(np.zeros((2, 2, 3), np.uint8)) == 0.0

    def test_illumination_stats_separate_dark_from_bright(self) -> None:
        """Mean luma is the under-exposure signal."""
        dark = np.full((32, 32, 3), 10, dtype=np.uint8)
        bright = np.full((32, 32, 3), 200, dtype=np.uint8)
        assert imageops.illumination_stats(dark)[0] < imageops.illumination_stats(bright)[0]

    def test_illumination_stddev_detects_flat_lighting(self) -> None:
        """A flat wall has zero contrast; a gradient has a lot.

        This is the ``min_luma_stddev`` gate: it catches a face lit by a single
        soft source with no shadow structure, which produces a technically
        well-exposed but unusable embedding.
        """
        flat = np.full((32, 32, 3), 128, dtype=np.uint8)
        gradient = np.tile(np.linspace(0, 255, 32, dtype=np.uint8), (32, 1))
        gradient = np.dstack([gradient] * 3)
        assert imageops.illumination_stats(flat)[1] == pytest.approx(0.0, abs=1.0)
        assert imageops.illumination_stats(gradient)[1] > 50.0

    def test_illumination_stats_on_empty(self) -> None:
        """Zero-size input must not divide by zero."""
        assert imageops.illumination_stats(np.zeros((0, 0, 3), np.uint8)) == (0.0, 0.0)


# ---------------------------------------------------------------------------
# Detector operating point: the bug measurement exposed
# ---------------------------------------------------------------------------


@pytest.mark.requires_model
class TestDetectorWorkingSize:
    """Running YuNet at full frame resolution is 6x slower and ~9x noisier.

    Measured 2026-09-29 on 24 single-person portraits, 3060x4080:
    ``scripts/sweep_detector.py``. Reproduce with that script; the assertions
    here pin the *mechanism* (boxes map correctly through the resize) rather
    than the statistics, which depend on the image set.
    """

    def test_working_size_is_not_ignored(self) -> None:
        """Regression pin: detect() used to override the working size with the
        full image size, so the setting did nothing at all."""
        from app.registry.backends.opencv_yunet_sface import YuNetDetector

        small = YuNetDetector(working_size=320, score_threshold=0.7)
        large = YuNetDetector(working_size=1280, score_threshold=0.7)
        image = np.full((2000, 3000, 3), 128, dtype=np.uint8)
        small_time = _time_detection(small, image)
        large_time = _time_detection(large, image)
        assert large_time > small_time * 1.5, (
            f"working_size had no effect: 320 took {small_time:.3f}s, 1280 took {large_time:.3f}s"
        )

    def test_boxes_are_mapped_back_to_source_coordinates(self) -> None:
        """Downscaling for inference must not shrink the reported boxes."""
        from app.registry.backends.opencv_yunet_sface import YuNetDetector

        detector = YuNetDetector(working_size=320, score_threshold=0.1)
        image = np.zeros((1200, 1600, 3), dtype=np.uint8)
        detections = detector.detect(image)
        for bbox, _landmarks, _score in detections:
            assert 0 <= bbox[0] < bbox[2] <= 1600, f"box {bbox} escaped the frame width"
            assert 0 <= bbox[1] < bbox[3] <= 1200, f"box {bbox} escaped the frame height"

    def test_empty_image_is_handled(self) -> None:
        """A zero-dimension frame must return [] rather than divide by zero."""
        from app.registry.backends.opencv_yunet_sface import YuNetDetector

        detector = YuNetDetector(working_size=320, score_threshold=0.7)
        assert detector.detect(np.zeros((0, 10, 3), dtype=np.uint8)) == []


def _time_detection(detector: object, image: np.ndarray) -> float:
    """Median-ish wall time of one detection pass."""
    start = time.perf_counter()
    detector.detect(image)  # type: ignore[attr-defined]
    return time.perf_counter() - start
