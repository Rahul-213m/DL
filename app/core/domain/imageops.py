"""Image ingestion boundary: decode, orientation, channel order.

Every image that reaches a detector or an embedder passes through this module.
That is deliberate. Two of the three defects in docs/00_audit.md were
channel-order and orientation bugs at exactly this boundary, and both were
invisible because they degraded quality rather than raising errors.

Channel order
-------------
Both model families in this project are OpenCV-based and expect **BGR**:

* YuNet and SFace are OpenCV DNN modules, natively BGR.
* InsightFace normalises with ``cv2.dnn.blobFromImage(..., swapRB=True)``, so
  its ONNX graphs receive BGR and swap to RGB internally.

The legacy pipeline decoded with Pillow (RGB) and passed it straight through,
transposing R and B relative to training. Because enrollment and inference were
*consistently* wrong, nearest-neighbour matching still mostly worked and nobody
noticed -- but absolute embedding quality dropped and, worse, every similarity
threshold calibrated on top of it became meaningless.

Orientation
-----------
A phone held in portrait stores the rotation in EXIF tag ``0x0112`` rather than
rotating the pixels. ``Image.open().convert("RGB")`` does not apply it. Since
the target device is a phone, this is the normal case, not an edge case.
"""

from __future__ import annotations

import io
import logging
from typing import Final

import cv2
import numpy as np
from PIL import Image, ImageOps

log = logging.getLogger(__name__)

#: EXIF tag holding the orientation transform (1-8).
EXIF_ORIENTATION_TAG: Final[int] = 0x0112

#: JPEG start-of-frame marker. Absence of this means "not a JPEG".
JPEG_MAGIC: Final[bytes] = b"\xff\xd8\xff"

#: Pixels. Guards against decompression bombs.
DEFAULT_MAX_PIXELS: Final[int] = 36_000_000


class ImageDecodeError(ValueError):
    """Raised when bytes are not a decodable, safe image."""


class ImageTooLargeError(ImageDecodeError):
    """Raised when an image exceeds the configured pixel budget."""


def to_bgr(rgb: np.ndarray) -> np.ndarray:
    """Convert an RGB array to BGR.

    No-op when the array has fewer than three channels (already greyscale).
    """
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError(f"expected (H, W, 3), got shape {rgb.shape}")
    return np.ascontiguousarray(rgb[:, :, ::-1])


def to_rgb(bgr: np.ndarray) -> np.ndarray:
    """Convert a BGR array to RGB."""
    if bgr.ndim != 3 or bgr.shape[2] != 3:
        raise ValueError(f"expected (H, W, 3), got shape {rgb_shape(bgr)}")
    return np.ascontiguousarray(bgr[:, :, ::-1])


def rgb_shape(array: np.ndarray) -> tuple[int, ...]:
    """Return an array's shape (small helper used in error messages)."""
    return tuple(array.shape)


def has_exif_orientation(data: bytes) -> int:
    """Return the raw EXIF orientation value, or 1 when absent.

    Reads the header only, so it is cheap enough to call on every upload.
    """
    try:
        with Image.open(io.BytesIO(data)) as image:
            return int(image.getexif().get(EXIF_ORIENTATION_TAG, 1) or 1)
    except (OSError, ValueError, SyntaxError):
        # A file that cannot be parsed simply has no orientation to report.
        return 1


def decode(data: bytes, *, max_pixels: int = DEFAULT_MAX_PIXELS) -> tuple[np.ndarray, dict[str, object]]:
    """Decode image bytes into a **BGR** array, honouring EXIF orientation.

    This is the single entry point for ingested images. Callers must not decode
    with Pillow directly.

    Args:
        data: Encoded image bytes.
        max_pixels: Reject anything larger, to bound memory on a hostile
            upload.

    Returns:
        ``(bgr_array, metadata)`` where metadata carries the original byte
        length, the pixel dimensions, whether a rotation was applied, and the
        raw EXIF orientation, so the frame record can record how the image was
        actually interpreted.

    Raises:
        ImageTooLargeError: pixel count exceeds ``max_pixels``.
        ImageDecodeError: not a decodable image.
    """
    if not data:
        raise ImageDecodeError("empty upload")

    raw_orientation = has_exif_orientation(data)

    try:
        with Image.open(io.BytesIO(data)) as image:
            if image.width * image.height > max_pixels:
                raise ImageTooLargeError(
                    f"image is {image.width}x{image.height} = "
                    f"{image.width * image.height:,} pixels, limit is {max_pixels:,}"
                )
            # Apply the orientation transform to the PIXELS. ImageOps.exif_transpose
            # is the only part of Pillow that handles all eight EXIF cases
            # correctly. It returns a NEW image whose concrete class may differ
            # from the file-backed original, hence the separate name.
            oriented = ImageOps.exif_transpose(image)
            rgb = np.asarray(oriented.convert("RGB"), dtype=np.uint8)
    except ImageTooLargeError:
        raise
    except Exception as exc:
        raise ImageDecodeError(f"could not decode image: {type(exc).__name__}") from exc

    applied = raw_orientation != 1
    if applied:
        log.info(
            "applied EXIF orientation",
            extra={"exif_orientation": raw_orientation, "shape_after": rgb.shape[:2]},
        )

    metadata: dict[str, object] = {
        "byte_length": len(data),
        "width": int(rgb.shape[1]),
        "height": int(rgb.shape[0]),
        "exif_orientation": raw_orientation,
        "orientation_applied": applied,
        "channel_order": "BGR",
    }
    return to_bgr(rgb), metadata


def encode_jpeg(image: np.ndarray, quality: int = 90) -> bytes:
    """Encode a BGR array to JPEG bytes.

    Used for crops and evidence frames. cv2 is used rather than Pillow because
    the array is already BGR and re-swapping channels here is how the original
    bug got introduced.
    """
    if not 1 <= quality <= 100:
        raise ValueError(f"jpeg quality must be 1-100, got {quality}")
    ok, buffer = cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    if not ok:  # pragma: no cover - cv2 returns False only on encoder failure
        raise ImageDecodeError("JPEG encoding failed")
    return buffer.tobytes()


def crop(image: np.ndarray, bbox: tuple[int, int, int, int]) -> np.ndarray:
    """Crop a BGR image, clamping the box to the image bounds.

    Clamping matters: a detector box can extend one pixel past the edge, and
    PIL's ``crop`` silently pads with black, which produces a corrupt crop
    rather than an error.
    """
    x1, y1, x2, y2 = bbox
    height, width = image.shape[:2]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(width, x2), min(height, y2)
    if x2 <= x1 or y2 <= y1:
        raise ImageDecodeError(f"degenerate crop {bbox} for image {width}x{height}")
    return np.ascontiguousarray(image[y1:y2, x1:x2])


def sharpness_score(crop_bgr: np.ndarray) -> float:
    """Variance of the Laplacian: the standard blur metric.

    Higher is sharper. Returns 0.0 for a crop too small to be meaningful.
    Interpretation is camera-specific, so the threshold is calibrated per
    deployment with ``scripts/calibrate_quality.py`` rather than assumed.
    """
    if crop_bgr.shape[0] < 3 or crop_bgr.shape[1] < 3:
        return 0.0
    grey = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(grey, cv2.CV_64F).var())


def illumination_stats(crop_bgr: np.ndarray) -> tuple[float, float]:
    """Return ``(mean_luma, luma_stddev)`` in 0-255 units.

    Mean detects under-exposure; standard deviation detects flat, low-contrast
    illumination. Both together catch more bad lighting than either alone.
    """
    if crop_bgr.size == 0:
        return 0.0, 0.0
    grey = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2GRAY)
    return float(grey.mean()), float(grey.std())


__all__ = [
    "DEFAULT_MAX_PIXELS",
    "EXIF_ORIENTATION_TAG",
    "ImageDecodeError",
    "ImageTooLargeError",
    "crop",
    "decode",
    "encode_jpeg",
    "has_exif_orientation",
    "illumination_stats",
    "sharpness_score",
    "to_bgr",
    "to_rgb",
]
