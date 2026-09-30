"""Registry construction, the production licence guard, and backend factories.

This is the single place that decides **which models are running**. Nothing
else in the codebase is permitted to import a model backend directly; it asks
the registry. That is what makes the licence guard airtight rather than
best-effort.
"""

from __future__ import annotations

import logging
import threading
from typing import Any

from app.core.config import settings
from app.registry.backends.insightface_buffalo_l import (
    InsightFaceDetector,
    InsightFaceEmbedder,
)
from app.registry.backends.licensed_stub import (
    UnconfiguredDetector,
    UnconfiguredEmbedder,
)
from app.registry.backends.liveness_stub import LivenessStub, NullLiveness
from app.registry.backends.opencv_yunet_sface import SFaceRecognizer, YuNetDetector
from app.registry.models import ModelDescriptor, ModelRegistry, NonCommercialModelError

log = logging.getLogger(__name__)


class LoadedRegistry:
    """A :class:`ModelRegistry` plus the constructed detector and embedder.

    Held as one object so the licences and the live models can never drift
    apart: they are built together and swapped atomically.

    The optional ``liveness`` attribute is the third model role. It is ``None``
    when no checker is configured, and a checker with ``supported`` False when
    only the development stub is available: the caller must be able to ask
    "did you actually check?" and get an honest answer either way.
    """

    def __init__(
        self,
        registry: ModelRegistry,
        detector: Any,
        embedder: Any,
        liveness: Any | None = None,
    ) -> None:
        self.registry = registry
        self.detector = detector
        self.embedder = embedder
        self.liveness = liveness

    def warmup(self) -> None:
        """Load both models eagerly, plus the checker if there is one."""
        self.detector.warmup()
        self.embedder.warmup()
        if self.liveness is not None:
            self.liveness.warmup()

    def shutdown(self) -> None:
        """Release any resources the backends hold."""
        for component in (self.detector, self.embedder):
            closer = getattr(component, "close", None)
            if callable(closer):
                closer()

    def describe(self) -> list[dict[str, Any]]:
        """Return a licence/accuracy summary for the observability endpoint."""
        rows = []
        for descriptor in (self.detector, self.embedder):
            if descriptor is None:
                continue
            name = getattr(descriptor, "name", "unknown")
            model = self.registry.get(name) if name in self.registry else None
            if model is None:
                continue
            rows.append(
                {
                    "key": model.key,
                    "kind": model.kind,
                    "version": model.version,
                    "license": model.license.license_name,
                    "commercial_use": model.license.commercial_use,
                    "training_data": model.license.training_data,
                    "sha256": model.license.sha256,
                    "embedding_dimension": model.embedding_dimension,
                    "legal_review_required": model.license.legal_review_required,
                    "shippable": model.shippable,
                }
            )
        return rows

    def describe_liveness(self) -> dict[str, Any]:
        """Report what, if anything, is checking for spoofed faces.

        Returned alongside :meth:`describe` on the models endpoint, because the
        honest answer to "is this deployment protected against a photo of a
        photo?" has to be visible without reading the source.
        """
        checker = self.liveness
        if checker is None:
            return {
                "configured": False,
                "performs_check": False,
                "backend": None,
                "enabled": settings.liveness_enabled,
            }
        return {
            "configured": True,
            "performs_check": bool(getattr(checker, "performs_check", getattr(checker, "supported", False))),
            "backend": getattr(checker, "name", "unknown"),
            "enabled": settings.liveness_enabled,
        }


# ---------------------------------------------------------------------------
# Backend factories
# ---------------------------------------------------------------------------

#: Detectors constructible by key. The combined buffalo_l entry is handled
#: specially because InsightFace packages detector and recogniser together.
_DETECTOR_FACTORIES: dict[str, Any] = {
    "opencv_yunet": lambda: YuNetDetector(score_threshold=settings.min_detection_score),
    "insightface_buffalo_l": InsightFaceDetector,
    "licensed_placeholder": UnconfiguredDetector,
}

_EMBEDDER_FACTORIES: dict[str, Any] = {
    "opencv_sface": SFaceRecognizer,
    "insightface_buffalo_l": InsightFaceEmbedder,
    "licensed_placeholder": UnconfiguredEmbedder,
}

#: Liveness checkers. Only the two honest options ship today; a real checker
#: is a drop-in class with ``check(image, bbox) -> float`` (ADR 0004).
_LIVENESS_FACTORIES: dict[str, Any] = {
    "stub": LivenessStub,
    "null": NullLiveness,
}

_lock = threading.Lock()
_loaded: LoadedRegistry | None = None


def _build(key: str, factories: dict[str, Any], role: str) -> Any:
    """Construct a backend by key with an actionable error on failure."""
    factory = factories.get(key)
    if factory is None:
        raise NonCommercialModelError(
            f"unknown {role} backend '{key}'; available: {sorted(factories)}. See docs/model_licensing.md."
        )
    return factory()


def load_registry(force: bool = False) -> LoadedRegistry:
    """Return the process-wide registry, building it on first use.

    Args:
        force: rebuild even if already loaded. Used by tests.

    Raises:
        NonCommercialModelError: if production is configured with weights that
            may not be used to serve a paying customer. This is the guard the
            CI release job also asserts against.
    """
    global _loaded
    with _lock:
        if _loaded is not None and not force:
            return _loaded

        registry = ModelRegistry()
        registry.load_from_config(settings.model_registry_config)

        # Enforce licensing BEFORE constructing anything that loads weights.
        # A non-commercial model must never even be downloaded in production.
        registry.assert_production_licensing(
            detector_key=settings.detector_backend,
            embedder_key=settings.embedder_backend,
            is_production=settings.is_production,
        )

        detector = _build(settings.detector_backend, _DETECTOR_FACTORIES, "detector")
        embedder = _build(settings.embedder_backend, _EMBEDDER_FACTORIES, "embedder")

        # The liveness slot is optional and absent by default. It is built even
        # when disabled so a misconfiguration is a startup error rather than a
        # surprise at the first suspected spoof.
        liveness = None
        if settings.liveness_backend:
            liveness = _build(settings.liveness_backend, _LIVENESS_FACTORIES, "liveness")

        _loaded = LoadedRegistry(
            registry=registry, detector=detector, embedder=embedder, liveness=liveness
        )
        log.info(
            "model registry loaded",
            extra={
                "detector": settings.detector_backend,
                "embedder": settings.embedder_backend,
                "liveness": settings.liveness_backend,
                "environment": settings.environment,
                "production": settings.is_production,
                "providers": settings.provider_list,
            },
        )
        return _loaded


def reset_registry() -> None:
    """Drop the cached registry. Used by tests."""
    global _loaded
    with _lock:
        _loaded = None


def current_descriptors() -> list[ModelDescriptor]:
    """Return the descriptors backing the currently loaded models."""
    if _loaded is None:
        return []
    return _loaded.registry.enabled_for_production(settings.detector_backend, settings.embedder_backend)


__all__ = [
    "LoadedRegistry",
    "current_descriptors",
    "load_registry",
    "reset_registry",
]
