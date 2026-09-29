import logging
from dataclasses import dataclass

import numpy as np

log = logging.getLogger(__name__)


@dataclass
class DetectedFace:
    bbox: tuple[int, int, int, int]
    embedding: np.ndarray
    detector_score: float


class InsightFaceRecognizer:
    """Lazy InsightFace adapter; model weights are never trained or modified."""

    def __init__(self):
        self._app = None

    def _load(self):
        if self._app is None:
            from insightface.app import FaceAnalysis  # type: ignore[import-untyped]

            from app.core.config import settings

            self._app = FaceAnalysis(
                name=settings.insightface_model, providers=settings.insightface_providers.split(",")
            )
            self._app.prepare(ctx_id=0, det_size=(1280, 1280))
        return self._app

    def warmup(self) -> None:
        """Load model files before the server starts accepting captures."""
        self._load()

    def detect(self, image: np.ndarray) -> list[DetectedFace]:
        faces = self._load().get(image)
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
