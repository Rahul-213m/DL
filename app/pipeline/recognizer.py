"""Legacy InsightFace adapter, retained as a thin shim over the ModelRegistry.

This module predates :mod:`app.registry`. It constructed an InsightFace
``FaceAnalysis`` directly, using settings fields (``insightface_model``,
``insightface_providers``) that W1 replaced with ``model_pack_name`` and
``onnx_providers`` in order to route every model through the registry and its
licence guard. That left this module **broken at runtime** -- mypy caught it
during W2:

    AttributeError: 'Settings' object has no attribute 'insightface_model'

Two things are fixed here:

1. It now delegates to the registry, so it inherits the production licence
   guard instead of bypassing it. Constructing it with a non-commercial backend
   in production raises, as it should.
2. **It converts to BGR before inference.** The legacy path fed Pillow RGB
   straight into InsightFace, whose ONNX graphs use ``swapRB=True`` and
   therefore expect BGR. W2 measured the cost of that bug at a 0.085
   separability deficit on the project's own enrollment photos
   (``scripts/measure_channel_order.py``).

**Deprecation.** W3 deletes this module along with the rest of the legacy
pipeline. New code must use :mod:`app.registry.loader` and
:mod:`app.core.domain.geometry` directly. It stays only so the existing
behavioural tests keep testing what they were written to test.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import numpy as np

from app.core.domain.imageops import to_bgr
from app.core.domain.types import BBox

log = logging.getLogger(__name__)


@dataclass
class DetectedFace:
    """One face returned by the legacy adapter.

    Retained because existing tests construct and consume this shape. W3
    replaces it with :class:`app.core.domain.types.FaceObservation`.
    """

    bbox: BBox
    embedding: np.ndarray
    detector_score: float


class InsightFaceRecognizer:
    """Shim over the registry's InsightFace backend.

    Model weights are never trained or modified. See ADR 0004 and
    docs/model_licensing.md.
    """

    def __init__(self) -> None:
        self._app: Any = None
        self._registry: Any = None

    def _load(self) -> Any:
        if self._app is None:
            from insightface.app import FaceAnalysis

            from app.core.config import settings
            from app.registry.loader import load_registry

            # Going through the registry means the commercial licence guard
            # runs. Previously this module constructed FaceAnalysis directly and
            # so could load non-commercial weights in production.
            self._registry = load_registry()
            app = FaceAnalysis(
                name=settings.model_pack_name,
                providers=settings.provider_list,
            )
            app.prepare(ctx_id=0, det_size=(1280, 1280))
            self._app = app
        return self._app

    def warmup(self) -> None:
        """Load model files before the server starts accepting captures."""
        self._load()

    def detect(self, image: np.ndarray) -> list[DetectedFace]:
        """Detect faces, accepting either RGB or BGR input.

        The channel order is ambiguous at this boundary, which is precisely why
        the ambiguity caused a silent quality regression. This shim takes RGB
        (what the legacy callers pass) and converts, and says so in its
        signature note. New code must pass BGR to the registry backend
        directly.
        """
        app = self._load()
        bgr = to_bgr(image)
        faces = app.get(bgr)
        results: list[DetectedFace] = []
        for f in faces:
            x1, y1, x2, y2 = (int(v) for v in f.bbox)
            results.append(
                DetectedFace(
                    bbox=(x1, y1, x2, y2),
                    embedding=np.asarray(f.embedding, dtype=np.float32),
                    detector_score=float(f.det_score),
                )
            )
        return results


recognizer = InsightFaceRecognizer()
