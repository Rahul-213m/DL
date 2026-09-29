"""InsightFace ``buffalo_l`` backend: SCRFD detector + ArcFace embedder.

**NON-COMMERCIAL. Dev and benchmark only.**

The registry refuses to start production with this enabled
(:meth:`ModelRegistry.assert_production_licensing`). The upstream licence
states the weights are "available for non-commercial research purposes only".
See docs/model_licensing.md.

Why it is retained
------------------
It is the accuracy reference. Every claim about how much accuracy the
permissive baseline gives up is measured against it, so it must stay runnable
in dev and CI. It is also what the legacy gallery was built with, which makes
it the only way to re-derive existing embeddings for comparison.

Channel order — the bug from docs/00_audit.md §4.1
-----------------------------------------------------
InsightFace normalises with ``cv2.dnn.blobFromImage(..., swapRB=True)``, which
means the ONNX graph expects **BGR** input. The legacy pipeline fed it RGB
straight from Pillow, transposing R and B relative to training.

:class:`InsightFaceBackend` fixes this by converting to BGR at the boundary and
exposing ``expects_channel_order = "BGR"``, so the ingestion layer cannot get
it wrong again. ``channel_order_regression`` in the test suite pins the fix.
"""

from __future__ import annotations

import logging
import threading
from typing import Any

import numpy as np

from app.core.domain.types import BBox, FloatArray

log = logging.getLogger(__name__)

#: What the underlying ONNX graphs actually expect, verified by reading
#: insightface/model_zoo/arcface_onnx.py:82 and retinaface.py:157 (swapRB=True).
EXPECTED_CHANNEL_ORDER = "BGR"


def to_bgr(image: np.ndarray) -> np.ndarray:
    """Convert an RGB array to BGR, no-op when already BGR.

    Used at the adapter boundary so no caller has to remember the convention.
    """
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(f"expected an (H, W, 3) image, got shape {image.shape}")
    return np.ascontiguousarray(image[:, :, ::-1])


class InsightFaceDetector:
    """SCRFD 10G, exposed through the same contract as every other detector."""

    name = "insightface_buffalo_l"
    #: BGR, unlike the legacy pipeline which fed RGB. See the module docstring.
    expects_channel_order = EXPECTED_CHANNEL_ORDER

    def __init__(self, det_size: int = 640, score_threshold: float = 0.5) -> None:
        self.det_size = det_size
        self.score_threshold = score_threshold
        self._lock = threading.Lock()
        self._app: Any = None

    def _ensure(self) -> Any:
        if self._app is None:
            from insightface.app import FaceAnalysis  # type: ignore[import-untyped]

            from app.core.config import settings

            self._app = FaceAnalysis(
                name=settings.model_pack_name,
                providers=settings.provider_list,
                allowed_modules=["detection"],
            )
            self._app.prepare(ctx_id=0, det_size=(self.det_size, self.det_size))
        return self._app

    def warmup(self) -> None:
        """Load weights eagerly."""
        self._ensure()

    def detect(self, image: np.ndarray) -> list[tuple[BBox, np.ndarray, float]]:
        """Detect faces in a **BGR** image."""
        app = self._ensure()
        with self._lock:
            faces = app.get(image, det_thresh=self.score_threshold)
        results: list[tuple[BBox, np.ndarray, float]] = []
        for face in faces:
            kps = getattr(face, "kps", None)
            landmarks = (
                np.asarray(kps, dtype=np.float32) if kps is not None else np.zeros((5, 2), dtype=np.float32)
            )
            x1, y1, x2, y2 = (int(v) for v in face.bbox)
            bbox: BBox = (x1, y1, x2, y2)
            results.append((bbox, landmarks, float(face.det_score)))
        return results


class InsightFaceEmbedder:
    """ArcFace R50 (w600k), 512-d L2-normalised."""

    name = "insightface_buffalo_l"
    dimension = 512
    expects_channel_order = EXPECTED_CHANNEL_ORDER

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._app: Any = None

    def _ensure(self) -> Any:
        if self._app is None:
            from insightface.app import FaceAnalysis  # type: ignore[import-untyped]

            from app.core.config import settings

            self._app = FaceAnalysis(
                name=settings.model_pack_name,
                providers=settings.provider_list,
                allowed_modules=["recognition"],
            )
            self._app.prepare(ctx_id=0, det_size=(640, 640))
        return self._app

    def warmup(self) -> None:
        """Load weights eagerly."""
        self._ensure()

    def embed(self, aligned_crop: np.ndarray) -> FloatArray:
        """Embed one **BGR** aligned 112x112 crop."""
        vector = self.embed_batch([aligned_crop])
        return vector[0]

    def embed_batch(self, aligned_crops: list[np.ndarray]) -> list[FloatArray]:
        """Embed many BGR aligned crops in a single ONNX batch.

        This is where InsightFace genuinely pays off: ``ArcFaceONNX.get_feat``
        takes a *list* of 112x112 images and builds one ``(N, 3, 112, 112)``
        blob, so a whole classroom frame's faces become a single session run
        instead of N. See insightface/model_zoo/arcface_onnx.py:72.
        """
        if not aligned_crops:
            return []
        app = self._ensure()
        net = _recognition_module(app)

        with self._lock:
            # get_feat applies (1/std) and swapRB=True for us, i.e. it expects
            # BGR input — which is what this adapter is given.
            out = net.get_feat([_conform(crop) for crop in aligned_crops])

        vectors: list[FloatArray] = []
        for row in np.asarray(out):
            vector = np.asarray(row, dtype=np.float32).reshape(-1)
            norm = float(np.linalg.norm(vector))
            if norm == 0 or not np.all(np.isfinite(vector)):
                raise ValueError("embedder produced a degenerate vector")
            vectors.append((vector / norm).astype(np.float32))
        return vectors


def _recognition_module(app: Any) -> Any:
    """Extract the recognition module from a prepared ``FaceAnalysis``.

    Raises:
        RuntimeError: if the model pack has no recognition module, which means
            the pack was loaded with the wrong ``allowed_modules``.
    """
    for module in app.models.values():
        if module.taskname == "recognition":
            return module
    raise RuntimeError(
        "recognition module missing from the model pack; allowed_modules must include 'recognition'"
    )


def _conform(crop: np.ndarray) -> np.ndarray:
    """Coerce a crop to the 112x112 uint8 BGR shape ArcFace expects."""
    import cv2

    if crop.dtype != np.uint8:
        crop = np.clip(crop, 0, 255).astype(np.uint8)
    if crop.ndim == 2:
        crop = cv2.cvtColor(crop, cv2.COLOR_GRAY2BGR)
    if crop.shape[0] != 112 or crop.shape[1] != 112:
        crop = cv2.resize(crop, (112, 112), interpolation=cv2.INTER_AREA)
    return np.ascontiguousarray(crop)


class CommercialModelNotLicensed(RuntimeError):
    """Raised if this backend is somehow constructed in production."""


__all__ = [
    "EXPECTED_CHANNEL_ORDER",
    "CommercialModelNotLicensed",
    "InsightFaceDetector",
    "InsightFaceEmbedder",
    "to_bgr",
]
