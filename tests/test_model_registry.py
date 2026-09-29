"""Tests for the model registry and the commercial licensing guard.

The guard is a legal control, not a configuration nicety, so it is tested the
way a legal control should be: adversarially, and against the exact
configuration a production deployment would use.
"""

from __future__ import annotations

import json

import pytest

from app.registry import loader
from app.registry.models import (
    BUILTIN_MODELS,
    LicenseMetadata,
    ModelDescriptor,
    ModelRegistry,
    NonCommercialModelError,
    TrainingProvenance,
)


class TestLicenseMetadata:
    """Licence facts must be recorded, not remembered."""

    def test_buffalo_l_is_flagged_non_commercial(self) -> None:
        """The InsightFace weights are non-commercial research only.

        Quoted upstream: "The training data containing the annotation (and the
        models trained with these data) are available for non-commercial
        research purposes only."
        """
        descriptor = BUILTIN_MODELS["insightface_buffalo_l"]
        assert descriptor.license.license_name == "InsightFace-NC"
        assert descriptor.license.commercial_use is False
        assert descriptor.shippable is False

    def test_buffalo_l_records_a_weight_hash(self) -> None:
        """A swapped weight file must be detectable."""
        assert len(BUILTIN_MODELS["insightface_buffalo_l"].license.sha256) == 64

    def test_permissive_baseline_is_commercially_usable(self) -> None:
        """YuNet is MIT and SFace is Apache-2.0, so both may ship."""
        for key in ("opencv_yunet", "opencv_sface"):
            assert BUILTIN_MODELS[key].shippable is True, key

    def test_sface_training_provenance_is_flagged_undocumented(self) -> None:
        """Apache-2.0 covers the files, not the training corpus. Must be flagged."""
        sface = BUILTIN_MODELS["opencv_sface"]
        assert sface.license.license_name == "Apache-2.0"
        assert sface.license.training_data == TrainingProvenance.UNDOCUMENTED.value
        assert sface.license.legal_review_required is True

    def test_every_model_records_provenance_and_a_source(self) -> None:
        """No model may be registered with an unknown origin."""
        for descriptor in ModelRegistry():
            assert descriptor.license.source_url, descriptor.key
            assert descriptor.license.training_data, descriptor.key
            assert descriptor.license.license_name, descriptor.key


class TestProductionGuard:
    """The guard must refuse non-commercial weights in production."""

    def test_production_refuses_buffalo_l(self) -> None:
        """Selling buffalo_l commercially is the exact failure this prevents."""
        registry = ModelRegistry()
        with pytest.raises(NonCommercialModelError) as exc:
            registry.assert_production_licensing("insightface_buffalo_l", "insightface_buffalo_l", True)
        message = str(exc.value)
        assert "insightface_buffalo_l" in message
        assert "docs/model_licensing.md" in message

    def test_production_refuses_non_commercial_detector_with_permissive_embedder(self) -> None:
        """A mixed pair is still refused; the detector is enough to block."""
        registry = ModelRegistry()
        with pytest.raises(NonCommercialModelError):
            registry.assert_production_licensing("insightface_buffalo_l", "opencv_sface", True)

    def test_production_allows_permissive_baseline(self) -> None:
        """The shipped default must pass, or the product cannot start."""
        registry = ModelRegistry()
        registry.assert_production_licensing("opencv_yunet", "opencv_sface", True)

    def test_development_allows_non_commercial(self) -> None:
        """Dev and benchmark need buffalo_l as the accuracy reference."""
        registry = ModelRegistry()
        registry.assert_production_licensing("insightface_buffalo_l", "insightface_buffalo_l", False)

    def test_staging_counts_as_production(self) -> None:
        """Staging holds real customer data and must obey the same rules."""
        registry = ModelRegistry()
        with pytest.raises(NonCommercialModelError):
            registry.assert_production_licensing("insightface_buffalo_l", "insightface_buffalo_l", True)
        # The config helper decides "production" for staging; assert that link.
        from app.core.config import Settings

        assert Settings(_env_file=None, environment="staging").is_production is True

    def test_unrecorded_placeholder_hash_blocks_production(self) -> None:
        """The placeholder must not ship until its real SHA-256 is recorded."""
        registry = ModelRegistry()
        with pytest.raises(NonCommercialModelError) as exc:
            registry.assert_production_licensing("licensed_placeholder", "licensed_placeholder", True)
        assert "SHA-256" in str(exc.value)

    def test_a_purchased_licence_clears_the_guard(self) -> None:
        """Recording a real licence must unblock, so the guard is not a dead end."""
        registry = ModelRegistry()
        registry.register(
            ModelDescriptor(
                key="licensed_placeholder",
                kind="detector+embedder",
                version="contract-2026",
                license=LicenseMetadata(
                    license_name="commercial-licensed",
                    commercial_use=True,
                    training_data=TrainingProvenance.FIRST_PARTY_CONSENTED.value,
                    source_url="contract://acme/2026-license",
                    sha256="a" * 64,
                    notes="Contract on file.",
                ),
                embedding_dimension=512,
            )
        )
        registry.assert_production_licensing("licensed_placeholder", "licensed_placeholder", True)

    def test_purchased_licence_can_be_recorded_via_config_file(self, tmp_path) -> None:
        """Operators must not have to edit Python to record a purchase."""
        overlay = tmp_path / "models.json"
        overlay.write_text(
            json.dumps(
                {
                    "models": {
                        "insightface_buffalo_l": {
                            "license": {
                                "license_name": "commercial-licensed",
                                "commercial_use": True,
                                "source_url": "contract://acme/2026",
                                "sha256": "b" * 64,
                            },
                            "version": "buffalo_l-commercial",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        registry = ModelRegistry()
        registry.load_from_config(overlay)
        registry.assert_production_licensing("insightface_buffalo_l", "insightface_buffalo_l", True)
        assert registry.get("insightface_buffalo_l").version == "buffalo_l-commercial"

    def test_unknown_backend_fails_loudly(self) -> None:
        """A typo must not silently fall back to something weaker."""
        registry = ModelRegistry()
        with pytest.raises(NonCommercialModelError, match="unknown model"):
            registry.assert_production_licensing("does_not_exist", "opencv_sface", True)

    def test_outstanding_legal_review_does_not_block_startup(self) -> None:
        """The permissive baseline must be able to ship.

        SFace's training-data provenance is undocumented. That is a real legal
        risk, but making it a start-up blocker would make the product
        unshippable, because it is the only commercially usable embedder
        available today. It is surfaced as an advisory instead, and the risk is
        tracked in docs/HUMAN_ACTIONS.md. This test exists so nobody quietly
        changes that trade-off without noticing it was deliberate.
        """
        registry = ModelRegistry()
        registry.assert_production_licensing("opencv_yunet", "opencv_sface", True)
        assert "opencv_sface" in registry.pending_legal_reviews()

    def test_pending_legal_reviews_lists_the_documented_ones(self) -> None:
        """The advisory surface must include both flagged models."""
        pending = set(ModelRegistry().pending_legal_reviews())
        assert {"insightface_buffalo_l", "opencv_sface"} <= pending

    def test_missing_weight_hash_blocks_even_a_permissive_licence(self) -> None:
        """Unrecorded provenance is a blocker regardless of the licence."""
        registry = ModelRegistry()
        registry.register(
            ModelDescriptor(
                key="opencv_sface",
                kind="embedder",
                version="2021dec",
                license=LicenseMetadata(
                    license_name="Apache-2.0",
                    commercial_use=True,
                    training_data=TrainingProvenance.UNDOCUMENTED.value,
                    source_url="https://github.com/opencv/opencv_zoo",
                    sha256="",
                ),
                embedding_dimension=128,
            )
        )
        with pytest.raises(NonCommercialModelError, match="SHA-256"):
            registry.assert_production_licensing("opencv_yunet", "opencv_sface", True)


class TestLoaderIntegration:
    """The guard must run before weights are loaded, not after."""

    def test_loader_rejects_non_commercial_in_production(self, monkeypatch, tmp_path) -> None:
        """End-to-end: production + buffalo_l must fail in load_registry()."""
        # Patch the environment field, not the is_production property: pydantic
        # v2 models do not allow a property to be shadowed via setattr.
        monkeypatch.setattr("app.core.config.settings.environment", "production")
        monkeypatch.setattr("app.registry.loader.settings.detector_backend", "insightface_buffalo_l")
        monkeypatch.setattr("app.registry.loader.settings.embedder_backend", "insightface_buffalo_l")
        loader.reset_registry()
        with pytest.raises(NonCommercialModelError):
            loader.load_registry(force=True)
        loader.reset_registry()

    def test_loader_builds_the_permissive_baseline(self, monkeypatch) -> None:
        """The default production path must construct real objects."""
        loader.reset_registry()
        loaded = loader.load_registry(force=True)
        try:
            assert loaded.detector.name == "opencv_yunet"
            assert loaded.embedder.name == "opencv_sface"
            assert loaded.embedder.dimension == 128
            rows = {row["key"] for row in loaded.describe()}
            assert rows == {"opencv_yunet", "opencv_sface"}
            assert all(row["commercial_use"] for row in loaded.describe())
        finally:
            loader.reset_registry()

    def test_placeholder_backend_raises_on_construction(self, monkeypatch) -> None:
        """Selecting the placeholder must fail loudly, never degrade silently."""
        from app.registry.backends.licensed_stub import (
            LicensedModelNotConfigured,
            UnconfiguredDetector,
        )

        with pytest.raises(LicensedModelNotConfigured, match=r"docs/model_licensing\.md"):
            UnconfiguredDetector()
