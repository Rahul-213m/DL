"""Drop-in slot for a commercially licensed model pack.

The operator supplies the weights and a short module that constructs the
backend; this file only holds the contract and a loud failure so an
unconfigured production deployment cannot quietly fall back to non-commercial
weights.

Expected operator contract
---------------------------
Place a module in ``app/registry/backends/`` exposing two factories::

    def build_detector(settings) -> Detector: ...
    def build_embedder(settings) -> Embedder: ...

and register it in :data:`app.registry.models.BUILTIN_MODELS` with real
licence metadata (including the weights SHA-256). Then set::

    DETECTOR_BACKEND=<your key>
    EMBEDDER_BACKEND=<your key>

See docs/model_licensing.md for the four routes to commercial compliance.
"""

from __future__ import annotations

import numpy as np

from app.core.domain.types import BBox, FloatArray


class LicensedModelNotConfigured(RuntimeError):
    """Raised when the licensed backend is selected but not implemented."""


_CONFIG_HINT = (
    "No commercially licensed model is configured.\n\n"
    "The production guard blocks the only fully featured backend "
    "(insightface_buffalo_l) because its weights are licensed for "
    "non-commercial research only.\n\n"
    "Resolve this by one of:\n"
    "  1. Using the permissive baseline (opencv_yunet + opencv_sface) —\n"
    "     commercially usable, weaker. See docs/benchmarks.md for the measured gap.\n"
    "  2. Purchasing a commercial InsightFace licence and implementing\n"
    "     build_detector/build_embedder in this package.\n"
    "  3. Registering a different licensed model via MODEL_REGISTRY_CONFIG.\n\n"
    "See docs/model_licensing.md and docs/HUMAN_ACTIONS.md item 1."
)


class UnconfiguredDetector:
    """A detector that refuses to run rather than silently degrading."""

    name = "licensed_placeholder"

    def __init__(self, *_args: object, **_kwargs: object) -> None:
        raise LicensedModelNotConfigured(_CONFIG_HINT)

    def warmup(self) -> None:
        """Always raises. Present only to satisfy the protocol."""
        raise LicensedModelNotConfigured(_CONFIG_HINT)

    def detect(self, image: np.ndarray) -> list[tuple[BBox, np.ndarray, float]]:  # noqa: ARG002
        """Always raises. Present only to satisfy the protocol."""
        raise LicensedModelNotConfigured(_CONFIG_HINT)


class UnconfiguredEmbedder:
    """An embedder that refuses to run rather than silently degrading."""

    name = "licensed_placeholder"
    dimension = 0

    def __init__(self, *_args: object, **_kwargs: object) -> None:
        raise LicensedModelNotConfigured(_CONFIG_HINT)

    def warmup(self) -> None:
        """Always raises. Present only to satisfy the protocol."""
        raise LicensedModelNotConfigured(_CONFIG_HINT)

    def embed(self, aligned_crop: np.ndarray) -> FloatArray:  # noqa: ARG002
        """Always raises. Present only to satisfy the protocol."""
        raise LicensedModelNotConfigured(_CONFIG_HINT)

    def embed_batch(self, aligned_crops: list[np.ndarray]) -> list[FloatArray]:  # noqa: ARG002
        """Always raises. Present only to satisfy the protocol."""
        raise LicensedModelNotConfigured(_CONFIG_HINT)


__all__ = ["LicensedModelNotConfigured", "UnconfiguredDetector", "UnconfiguredEmbedder"]
