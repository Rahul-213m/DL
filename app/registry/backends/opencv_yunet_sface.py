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
#: YuNet reference working size. The default used in production is 640; see
#: YuNetDetector for the measured trade-off.
YUNET_REFERENCE_SIZE = 320
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

    Operating point (MEASURED 2026-09-29, see docs/benchmarks.md)
    ------------------------------------------------------------
    YuNet is designed for a small input (the reference demo uses 320x320). It
    is a fully-convolutional net, so feeding it a 12 MP frame "works", but it
    is both slow and noisy: on single-person portrait photos it reported a
    mean of 2.62 faces at threshold 0.6, i.e. 1.62 false positives per image.

    The fix is to **scale the image down to the working size, detect, and map
    the boxes back**. Face scale within the network is then consistent with
    training, which is what the detector's receptive field expects.

    There is a real trade-off here, recorded honestly in docs/benchmarks.md:
    a smaller working size finds small faces better (they survive the
    downscale) but is worse at separating nearby large faces. ``working_size``
    is therefore configuration, not a constant.

    Thread safety: a single ``cv2.FaceDetectorYN`` is not documented as
    thread-safe, so a lock serialises inference. Concurrency comes from the
    job-queue level instead.
    """

    name = "opencv_yunet"

    def __init__(
        self,
        working_size: int = 640,
        score_threshold: float = 0.7,
        nms_threshold: float = 0.3,
        top_k: int = 5000,
    ) -> None:
        self.working_size = working_size
        self.score_threshold = score_threshold
        self.nms_threshold = nms_threshold
        self.top_k = top_k
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
                [self.working_size, self.working_size],
                self.score_threshold,
                self.nms_threshold,
                self.top_k,
            )
        return self._net

    def warmup(self) -> None:
        """Load the network and run one throwaway inference."""
        self.detect(np.zeros((self.working_size, self.working_size, 3), dtype=np.uint8))

    def set_working_size(self, size: int) -> None:
        """Change the network input size. Takes effect on the next call."""
        if size != self.working_size:
            self.working_size = size
            self._net = None  # force recreation with the new size

    def detect(self, image: np.ndarray) -> list[tuple[BBox, np.ndarray, float]]:
        """Detect faces in a **BGR** image.

        The image is downscaled so its shorter side is ``working_size``, faces
        are found at that scale, then boxes and landmarks are mapped back to
        source-image pixels so every downstream coordinate stays in one space.

        Args:
            image: ``(H, W, 3)`` uint8 BGR array.

        Returns:
            ``[(bbox, landmarks[N,2] float32, score), ...]`` in source coords.
        """
        if image.dtype != np.uint8:
            image = np.clip(image, 0, 255).astype(np.uint8)
        height, width = image.shape[:2]
        if height == 0 or width == 0:
            return []

        scale = self.working_size / float(min(height, width))
        if scale < 1.0:
            # Downscale: preserves small faces better than upscaling does.
            net_w = max(self.working_size, round(width * scale))
            net_h = max(self.working_size, round(height * scale))
            resized = cv2.resize(image, (net_w, net_h), interpolation=cv2.INTER_AREA)
        else:
            net_w, net_h = width, height
            resized = image

        net = self._ensure()
        with self._lock:
            net.setInputSize((net_w, net_h))
            _, faces = net.detect(resized)

        if faces is None:
            return []

        # Map back to source coordinates. scale_x and scale_y differ because
        # only the shorter side was normalised.
        scale_x = width / float(net_w)
        scale_y = height / float(net_h)

        results: list[tuple[BBox, np.ndarray, float]] = []
        for face in faces:
            # YuNet returns integral x/y/w/h; int() keeps numpy ints out of BBox.
            x, y, w, h = (int(v) for v in face[:4])
            score = float(face[-1])
            landmarks = np.asarray(face[4 : 4 + YUNET_LANDMARKS * 2], dtype=np.float32).reshape(
                YUNET_LANDMARKS, 2
            ) * np.array([scale_x, scale_y], dtype=np.float32)
            bbox: BBox = (
                round(x * scale_x),
                round(y * scale_y),
                round((x + w) * scale_x),
                round((y + h) * scale_y),
            )
            results.append((bbox, landmarks, score))
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
