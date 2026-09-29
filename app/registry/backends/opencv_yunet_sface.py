"""OpenCV YuNet detector + SFace recogniser: the permissive-licence baseline.

Licence
-------
* YuNet — MIT (opencv_zoo states every file in that directory is MIT).
* SFace — Apache-2.0 (same source). **Training-data provenance is undocumented**;
  flagged NEEDS LAWYER in docs/model_licensing.md.

Channel order
-------------
OpenCV's DNN module is BGR-native. ``YuNetNet`` and ``SFaceRecognizer`` both take
BGR input, which matches what ``cv2.imdecode`` and the video capture produce.
This backend therefore **requires BGR** and the ingestion layer is responsible
for handing it BGR. Contrast with the InsightFace backend, which has its own
(incorrect, see docs/00_audit.md §4.1) expectations.

This is the backend that must work in production, so it is also the one with
the most tests.
"""

from __future__ import annotations

import logging
import threading
from pathlib import Path

import cv2
import numpy as np

from app.core.domain.types import BBox, FloatArray

log = logging.getLogger(__name__)

#: SFace input size. Fixed by the model.
SFACE_INPUT_SIZE = (112, 112)
#: YuNet's native working resolution. The model is fully convolutional and
#: scales; larger inputs find smaller faces but cost more.
YUNET_INPUT_SIZE = (320, 320)
#: YuNet's landmark count: left eye, right eye, nose, left mouth, right mouth.
YUNET_LANDMARKS = 5


class ModelFileMissing(RuntimeError):
    """Raised when a weight file is absent, with instructions to fetch it."""


def _resolve_weights(local_path: str | None, env_var: str, hint_url: str) -> Path:
    """Locate a weight file, searching ``MODELS_DIR`` then ``models/``.

    Raises:
        ModelFileMissing: when the file cannot be found. The message carries
            the download command so the failure is self-explanatory.
    """
    candidates: list[Path] = []
    if local_path:
        candidates.append(Path(local_path))
        root = Path(__import__("os").environ.get("MODELS_DIR", "models"))
        candidates.append(root / local_path)
    import os

    override = os.environ.get(env_var)
    if override:
        candidates.insert(0, Path(override))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    searched = ", ".join(str(c) for c in candidates)
    raise ModelFileMissing(
        f"model weights not found (searched: {searched}).\n"
        f"Fetch them with:  curl -L -o models/{local_path} {hint_url}"
    )


class YuNetDetector:
    """Face detector built on OpenCV's YuNet.

    Thread safety: a single ``cv2.FaceDetectorYN`` instance is NOT documented as
    thread-safe, so a lock serialises inference. Inference on CPU is fast enough
    (single-digit milliseconds for a 640x480 tile) that contention is not the
    bottleneck; batch parallelism happens at the job-queue level instead.
    """

    name = "opencv_yunet"

    def __init__(self, input_size: tuple[int, int] = YUNET_INPUT_SIZE, score_threshold: float = 0.6) -> None:
        self.input_size = input_size
        self.score_threshold = score_threshold
        self._lock = threading.Lock()
        self._net: cv2.FaceDetectorYN | None = None
        self._path: Path | None = None

    def _ensure(self) -> cv2.FaceDetectorYN:
        if self._net is None:
            self._path = _resolve_weights(
                "yunet_2023mar.onnx",
                "YUNET_MODEL_PATH",
                "https://github.com/opencv/opencv_zoo/raw/main/models/"
                "face_detection_yunet/face_detection_yunet_2023mar.onnx",
            )
            self._net = cv2.FaceDetectorYN.create(
                str(self._path),
                "",
                [self.input_size[0], self.input_size[1]],
                self.score_threshold,
                0.3,  # NMS threshold
                5000,  # top-k before NMS
            )
        return self._net

    def warmup(self) -> None:
        """Load the network and run one throwaway inference."""
        self.detect(np.zeros((self.input_size[1], self.input_size[0], 3), dtype=np.uint8))

    def set_input_size(self, size: tuple[int, int]) -> None:
        """Change the working resolution. Takes effect on the next call."""
        if size != self.input_size:
            self.input_size = size
            self._net = None  # force recreation with the new size

    def detect(self, image: np.ndarray) -> list[tuple[BBox, np.ndarray, float]]:
        """Detect faces in a **BGR** image.

        Args:
            image: ``(H, W, 3)`` uint8 BGR array.

        Returns:
            ``[(bbox, landmarks[N,2] float32, score), ...]``.
        """
        if image.dtype != np.uint8:
            image = np.clip(image, 0, 255).astype(np.uint8)
        height, width = image.shape[:2]

        net = self._ensure()
        with self._lock:
            # setInputSize must be re-issued whenever the image changes size.
            net.setInputSize((width, height))
            _, faces = net.detect(image)

        if faces is None:
            return []

        results: list[tuple[BBox, np.ndarray, float]] = []
        for face in faces:
            # YuNet returns integral x/y/w/h; int() keeps numpy ints out of BBox.
            x, y, w, h = (round(int(v)) for v in face[:4])
            score = float(face[-1])
            landmarks = np.asarray(face[4 : 4 + YUNET_LANDMARKS * 2], dtype=np.float32).reshape(
                YUNET_LANDMARKS, 2
            )
            results.append(((x, y, x + w, y + h), landmarks, score))
        return results


class SFaceRecognizer:
    """Face embedder built on OpenCV's SFace (MobileFaceNet + SFace loss).

    Produces 128-d L2-normalised embeddings. That is a **quarter** the dimension
    of ArcFace's 512-d, which is the single largest source of the accuracy gap
    against buffalo_l. It is a deliberate trade: 128-d is 4x cheaper to store,
    search and transmit, which matters more at 300 students than the last few
    points of TAR. See docs/benchmarks.md for the measured comparison.
    """

    name = "opencv_sface"
    dimension = 128

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._net: cv2.FaceRecognizerSF | None = None

    def _ensure(self) -> cv2.FaceRecognizerSF:
        if self._net is None:
            path = _resolve_weights(
                "sface_2021dec.onnx",
                "SFACE_MODEL_PATH",
                "https://github.com/opencv/opencv_zoo/raw/main/models/"
                "face_recognition_sface/face_recognition_sface_2021dec.onnx",
            )
            self._net = cv2.FaceRecognizerSF.create(str(path), "")
        return self._net

    def warmup(self) -> None:
        """Load the network and run one throwaway inference."""
        self.embed(np.zeros((SFACE_INPUT_SIZE[1], SFACE_INPUT_SIZE[0], 3), dtype=np.uint8))

    def embed(self, aligned_crop: np.ndarray) -> FloatArray:
        """Embed one **BGR** aligned 112x112 crop.

        Returns:
            Unit-norm float32 vector of length 128.
        """
        net = self._ensure()
        crop = self._conform(aligned_crop)
        with self._lock:
            feature = net.feature(crop)
        vector = np.asarray(feature, dtype=np.float32).reshape(-1)
        norm = float(np.linalg.norm(vector))
        if norm == 0 or not np.all(np.isfinite(vector)):
            raise ValueError("embedder produced a degenerate vector")
        return (vector / norm).astype(np.float32)

    def embed_batch(self, aligned_crops: list[np.ndarray]) -> list[FloatArray]:
        """Embed many crops.

        SFace exposes only a single-image ``feature``; this loops. The win over
        a per-crop call at the pipeline level comes from amortising decode and
        alignment, which the caller does. Recorded here so the interface is
        honoured even where the backend cannot honour the batching.
        """
        return [self.embed(crop) for crop in aligned_crops]

    @staticmethod
    def _conform(crop: np.ndarray) -> np.ndarray:
        """Coerce any crop into the exact shape and dtype SFace expects."""
        if crop.dtype != np.uint8:
            crop = np.clip(crop, 0, 255).astype(np.uint8)
        if crop.shape[0] != SFACE_INPUT_SIZE[1] or crop.shape[1] != SFACE_INPUT_SIZE[0]:
            crop = cv2.resize(crop, SFACE_INPUT_SIZE, interpolation=cv2.INTER_AREA)
        if crop.ndim == 2:
            crop = cv2.cvtColor(crop, cv2.COLOR_GRAY2BGR)
        return np.ascontiguousarray(crop)


__all__ = ["SFACE_INPUT_SIZE", "ModelFileMissing", "SFaceRecognizer", "YuNetDetector"]
