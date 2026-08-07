from collections.abc import Mapping
from typing import Any

from .classification_result import ClassificationResult
from .discovery import WalletDiscoveryResult
from .wallet_classifier import WalletClassifier
from .wallet_profile import WalletProfile


class WalletClassificationEngine:
    """Classify discovered wallet profiles with deterministic rules."""

    def __init__(self, classifier: WalletClassifier | None = None) -> None:
        self.classifier = classifier or WalletClassifier()

    def classify(
        self,
        discovered: WalletDiscoveryResult,
        metadata: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> tuple[ClassificationResult, ...]:
        metadata = metadata or {}
        return tuple(
            ClassificationResult(profile, self.classifier.classify(profile, metadata.get(profile.wallet.wallet_id)))
            for profile in discovered.profiles
        )
