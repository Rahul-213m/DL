"""Model descriptors, license metadata and the registry.

The registry exists because of one hard commercial constraint: **face model
weights are licensed separately from their code**, and the two differ. The
InsightFace Python package is MIT, but the ``buffalo_l`` weights it downloads
are explicitly "for non-commercial research purposes only". A product sold to
colleges cannot ship those weights.

Every model therefore carries licence metadata, and production refuses to start
if an enabled model is not commercially usable.

Licence facts below were verified against upstream sources on **2026-09-29**;
see docs/model_licensing.md for the full analysis and the quoted text.
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from dataclasses import dataclass, field, replace
from enum import StrEnum
from pathlib import Path

log = logging.getLogger(__name__)


class ModelLicense(StrEnum):
    """How a model's weights may be used.

    The distinction that matters legally is between a licence that permits
    commercial use and one that does not. Code licences (MIT, Apache-2.0)
    describe the *implementation*; a permissive code licence does NOT make
    non-permissive *weights* usable.
    """

    MIT = "MIT"
    APACHE_2 = "Apache-2.0"
    #: InsightFace pretrained packs. Non-commercial research only.
    INSIGHTFACE_NON_COMMERCIAL = "InsightFace-NC"
    #: No licence has been identified. Treat as unusable until cleared.
    UNKNOWN = "unknown"
    #: You hold a commercial licence. Record the contract reference.
    COMMERCIAL_LICENSED = "commercial-licensed"


class TrainingProvenance(StrEnum):
    """Where the training data came from. Drives the privacy risk assessment."""

    #: Public, non-personal, explicitly permitted for research and commercial.
    PUBLIC_ACADEMIC = "public-academic"
    #: Web-scraped face images. Licence and privacy both unclear.
    WEB_SCRAPED = "web-scraped"
    #: Not documented by the publisher.
    UNDOCUMENTED = "undocumented"
    #: Your own consented data.
    FIRST_PARTY_CONSENTED = "first-party-consented"


@dataclass(frozen=True, slots=True)
class LicenseMetadata:
    """Provenance and usage rights for one set of weights.

    Attributes:
        license_name: SPDX-like identifier or a descriptive licence name.
        commercial_use: Whether a paying customer may be served using these
            weights. This is the field the production guard reads.
        training_data: Provenance of the training corpus.
        source_url: Where the weights were obtained.
        sha256: Hash of the weight file(s), so a swapped file is detected.
        notes: Free text for the legal file.
        legal_review_required: True when a lawyer must confirm before use.
    """

    license_name: str
    commercial_use: bool
    #: Kept as a plain string so a JSON overlay can supply it without an enum.
    training_data: str
    source_url: str
    sha256: str
    notes: str = ""
    legal_review_required: bool = False


@dataclass(frozen=True, slots=True)
class ModelDescriptor:
    """One registered model: what it does, where it comes from, what it costs.

    Attributes:
        key: Stable identifier used in configuration (``DETECTOR_BACKEND``).
        kind: "detector" or "embedder".
        version: Model version string.
        license: Licence metadata for the **weights**.
        embedding_dimension: Only meaningful for embedders.
        accuracy_reference: The publisher's own claimed metric, with its
            dataset named. Recorded for comparison only; never presented as
            our measured accuracy.
        recommended_min_face_px: Below this the model degrades sharply.
        local_path: Path to weights relative to the models root.
        license_blocker: Human-readable reason this model cannot ship in
            production, or ``None`` if it can.
    """

    key: str
    kind: str
    version: str
    license: LicenseMetadata
    embedding_dimension: int | None = None
    accuracy_reference: str | None = None
    recommended_min_face_px: int = 40
    local_path: str | None = None
    license_blocker: str | None = None
    extra: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Derive ``license_blocker`` when the caller did not set one."""
        if self.license_blocker is None and not self.license.commercial_use:
            object.__setattr__(
                self,
                "license_blocker",
                f"weights are {self.license.license_name}, which is not licensed for commercial use",
            )

    @property
    def shippable(self) -> bool:
        """Whether these weights may be used to serve a paying customer."""
        return self.license.commercial_use


# ---------------------------------------------------------------------------
# Registered models
# ---------------------------------------------------------------------------
# Hashes measured 2026-09-29 by `sha256sum` on the downloaded weight files.

INSIGHTFACE_BUFFALO_L_LICENSE = LicenseMetadata(
    license_name=ModelLicense.INSIGHTFACE_NON_COMMERCIAL.value,
    commercial_use=False,
    training_data=TrainingProvenance.WEB_SCRAPED.value,
    source_url="https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip",
    sha256="5838f7fe053675b1c7a08b633df49e7af5495cee0493c7dcf6697200b85b5b91",  # det_10g.onnx (SCRFD)
    notes=(
        "Code is MIT. Weights are explicitly 'for non-commercial research purposes only'. "
        "Upstream states: 'The training data containing the annotation (and the models "
        "trained with these data) are available for non-commercial research purposes only.' "
        "Commercial licensing contact published upstream: recognition-oss-pack@insightface.ai. "
        "SHA-256 recorded is for the SCRFD detector det_10g.onnx; the ArcFace recogniser "
        "w600k_r50.onnx is 4c06341c33c2ca1f86781dab0e829f88ad5b64be9fba56e56bc9ebdefc619e43. "
        "Dev and benchmark use only. Never enable in production."
    ),
    legal_review_required=True,
)

YUNET_LICENSE = LicenseMetadata(
    license_name=ModelLicense.MIT.value,
    commercial_use=True,
    training_data=TrainingProvenance.PUBLIC_ACADEMIC.value,
    source_url=(
        "https://github.com/opencv/opencv_zoo/blob/main/models/face_detection_yunet/"
        "face_detection_yunet_2023mar.onnx"
    ),
    sha256="8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4",
    notes=(
        "opencv_zoo states: 'All files in this directory are licensed under MIT License'. "
        "Upstream reports WIDER Face validation AP_easy 0.834 / AP_medium 0.824 / AP_hard 0.708 "
        "in the model card. Published training set is libfacedetection.train (research "
        "release), which is consistent with the MIT grant over the released files."
    ),
)

SFACE_LICENSE = LicenseMetadata(
    license_name=ModelLicense.APACHE_2.value,
    commercial_use=True,
    training_data=TrainingProvenance.UNDOCUMENTED.value,
    source_url=(
        "https://github.com/opencv/opencv_zoo/blob/main/models/face_recognition_sface/"
        "face_recognition_sface_2021dec.onnx"
    ),
    sha256="0ba9fbfa01b5270c96627c4ef784da859931e02f04419c829e83484087c34e79",
    notes=(
        "opencv_zoo states: 'All files in this directory are licensed under Apache 2.0 License'. "
        "Architecture is MobileFaceNet trained with the SFace loss (arXiv:2205.12010). "
        "CAVEAT: the publisher does NOT document which images were used for training. "
        "Apache-2.0 covers the released files, not the provenance of the training corpus. "
        "Flagged NEEDS LAWYER before any commercial launch."
    ),
    legal_review_required=True,
)

#: Placeholder for a commercially licensed pack the operator supplies.
LICENSED_PLACEHOLDER_LICENSE = LicenseMetadata(
    license_name=ModelLicense.COMMERCIAL_LICENSED.value,
    commercial_use=True,
    training_data=TrainingProvenance.UNDOCUMENTED.value,
    source_url="contract://operator-supplied",
    sha256="<replace-with-sha256-of-supplied-weights>",
    notes=(
        "Drop-in slot for a commercially licensed InsightFace pack or any other "
        "licensed detector/embedder. Populate SHA256 of the supplied weights before "
        "enabling in production; the registry refuses an unreplaced placeholder."
    ),
    legal_review_required=True,
)


BUILTIN_MODELS: dict[str, ModelDescriptor] = {
    "insightface_buffalo_l": ModelDescriptor(
        key="insightface_buffalo_l",
        kind="detector+embedder",
        version="buffalo_l",
        license=INSIGHTFACE_BUFFALO_L_LICENSE,
        embedding_dimension=512,
        accuracy_reference=("Publisher benchmark (IJB-C, InsightFace model zoo). NOT our measurement."),
        recommended_min_face_px=40,
        local_path=None,  # resolved by insightface into ~/.insightface
    ),
    "opencv_yunet": ModelDescriptor(
        key="opencv_yunet",
        kind="detector",
        version="2023mar",
        license=YUNET_LICENSE,
        recommended_min_face_px=10,
        local_path="yunet_2023mar.onnx",
        accuracy_reference=(
            "Publisher benchmark (WIDER Face val): AP_easy 0.834 / AP_medium 0.824 / "
            "AP_hard 0.708. NOT our measurement."
        ),
    ),
    "opencv_sface": ModelDescriptor(
        key="opencv_sface",
        kind="embedder",
        version="2021dec",
        license=SFACE_LICENSE,
        embedding_dimension=128,
        recommended_min_face_px=50,
        local_path="sface_2021dec.onnx",
        accuracy_reference=(
            "Publisher benchmark (opencv_zoo tools/eval): accuracy 0.9940. NOT our measurement, "
            "and the eval set is not stated."
        ),
    ),
    "licensed_placeholder": ModelDescriptor(
        key="licensed_placeholder",
        kind="detector+embedder",
        version="operator-supplied",
        license=LICENSED_PLACEHOLDER_LICENSE,
        embedding_dimension=None,
        local_path=None,
    ),
}


class ModelRegistry:
    """Lookup of model descriptors by key, plus the production licence guard."""

    def __init__(self, models: dict[str, ModelDescriptor] | None = None) -> None:
        self._models = dict(models if models is not None else BUILTIN_MODELS)

    def __contains__(self, key: object) -> bool:
        """Whether ``key`` is registered."""
        return key in self._models

    def __iter__(self) -> Iterator[ModelDescriptor]:
        """Iterate over every registered descriptor."""
        return iter(self._models.values())

    def get(self, key: str) -> ModelDescriptor:
        """Return a descriptor or raise ``KeyError`` listing valid keys."""
        try:
            return self._models[key]
        except KeyError:
            raise KeyError(f"unknown model '{key}'; registered: {sorted(self._models)}") from None

    def register(self, descriptor: ModelDescriptor) -> None:
        """Add or replace a descriptor."""
        self._models[descriptor.key] = descriptor

    def enabled_for_production(self, detector_key: str, embedder_key: str) -> list[ModelDescriptor]:
        """Return the descriptors that would be active in a production run.

        Raises:
            KeyError: if either key is not registered. A typo must fail loudly
                rather than silently select a different, weaker model.
        """
        keys = [k for k in (detector_key, embedder_key) if k]
        found: list[ModelDescriptor] = []
        for key in keys:
            descriptor = self.get(key)
            # A combined detector+embedder key contributes both roles.
            if descriptor not in found:
                found.append(descriptor)
        return found

    def assert_production_licensing(
        self,
        detector_key: str,
        embedder_key: str,
        is_production: bool,
    ) -> None:
        """Refuse weights that may not lawfully serve a paying customer.

        Two things are **hard blockers**, because shipping them would be
        unlawful, not merely risky:

        1. A licence that forbids commercial use.
        2. Provenance that was never recorded (no weights SHA-256).

        One thing is **not** a blocker: ``legal_review_required``. A permissive
        licence (MIT / Apache-2.0) permits commercial use; the open question is
        whether the training corpus is clean. Blocking startup on that would
        make the product unshippable, because the permissive baseline is the only
        backend that can lawfully ship today. Instead it is surfaced loudly —
        logged at WARNING, returned by ``/health/models``, listed in
        docs/HUMAN_ACTIONS.md — so the operator can act on it without the
        product being dead in the water. This is an engineering trade, and it is
        flagged as NEEDS LAWYER in docs/model_licensing.md.

        Raises:
            NonCommercialModelError: on a hard blocker, or on an unknown key.
        """
        if not is_production:
            return

        try:
            descriptors = self.enabled_for_production(detector_key, embedder_key)
        except KeyError as exc:
            raise NonCommercialModelError(
                f"{exc}. Check DETECTOR_BACKEND and EMBEDDER_BACKEND. "
                "Available: insightface_buffalo_l, opencv_yunet, opencv_sface, "
                "licensed_placeholder. See docs/model_licensing.md."
            ) from exc

        blockers: list[str] = []
        advisories: list[str] = []

        for descriptor in descriptors:
            reasons: list[str] = []
            if not descriptor.shippable:
                reasons.append(
                    descriptor.license_blocker
                    or f"weights are {descriptor.license.license_name}, "
                    "which is not licensed for commercial use"
                )
            if not descriptor.license.sha256 or "<replace-with-sha256" in descriptor.license.sha256:
                reasons.append("weights SHA-256 has not been recorded")
            if reasons:
                blockers.append(f"  - {descriptor.key} ({descriptor.version}): " + "; ".join(reasons))
            elif descriptor.license.legal_review_required:
                advisories.append(
                    f"  - {descriptor.key} ({descriptor.version}): licence "
                    f"{descriptor.license.license_name} permits commercial use, but training-data "
                    f"provenance is '{descriptor.license.training_data}' and legal review is "
                    "outstanding. Tracked in docs/HUMAN_ACTIONS.md."
                )

        for advisory in advisories:
            log.warning("model licence advisory (non-blocking):%s", advisory)

        if blockers:
            raise NonCommercialModelError(
                "Refusing to start: the configured models cannot lawfully serve a "
                "paying customer.\n" + "\n".join(blockers) + "\n\n"
                "This product is sold commercially. Fix by either:\n"
                "  1. Setting DETECTOR_BACKEND=opencv_yunet and "
                "EMBEDDER_BACKEND=opencv_sface, or\n"
                "  2. Purchasing a commercial licence and recording it via "
                "MODEL_REGISTRY_CONFIG, or\n"
                "  3. Running with ENVIRONMENT=development (dev and benchmark only).\n\n"
                "See docs/model_licensing.md."
            )

    def pending_legal_reviews(self) -> list[str]:
        """Keys whose licence permits use but whose legal review is outstanding.

        Surfaced on ``/health/models`` so an operator always sees the open
        legal items without reading the source.
        """
        return [d.key for d in self._models.values() if d.license.legal_review_required]

    def load_from_config(self, config_path: str | Path | None = None) -> None:
        """Load an optional YAML/JSON overlay of model metadata.

        Lets an operator record a purchased licence without editing code.
        """
        if config_path is None:
            return
        import json
        from pathlib import Path as _Path

        path = _Path(config_path)
        if not path.is_file():
            return
        raw = json.loads(path.read_text(encoding="utf-8"))
        for key, patch in raw.get("models", {}).items():
            base = self.get(key)
            lic = base.license
            if "license" in patch:
                lic = replace(lic, **{k: v for k, v in patch["license"].items() if k != "license_name"})
                lic = replace(lic, license_name=patch["license"].get("license_name", lic.license_name))
            # ModelDescriptor uses slots, so merge via replace() rather than
            # touching __dict__.
            self.register(
                replace(base, key=key, license=lic, **{k: v for k, v in patch.items() if k != "license"})
            )


class NonCommercialModelError(RuntimeError):
    """Raised when production is configured with non-commercial weights."""


__all__ = [
    "BUILTIN_MODELS",
    "INSIGHTFACE_BUFFALO_L_LICENSE",
    "LICENSED_PLACEHOLDER_LICENSE",
    "SFACE_LICENSE",
    "YUNET_LICENSE",
    "LicenseMetadata",
    "ModelDescriptor",
    "ModelLicense",
    "ModelRegistry",
    "NonCommercialModelError",
    "TrainingProvenance",
]
