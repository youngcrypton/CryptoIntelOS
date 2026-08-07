from typing import Protocol

from src.wallet_intelligence import LabelType

from .whale_score import (
    BehaviorScore,
    CapitalScore,
    ConfidenceScore,
    CrossChainScore,
    HistoricalScore,
    InfluenceScore,
    NetworkScore,
    WhaleScoreSet,
)


Metrics = tuple[tuple[str, float], ...]


class ScoringStrategy(Protocol):
    """Pluggable strategy for independent Whale Intelligence dimensions."""

    def score(self, classifications: tuple[LabelType, ...], metrics: Metrics) -> WhaleScoreSet: ...


class DeterministicScoringStrategy:
    """Read explicit dimension values without combining them."""

    DIMENSIONS = ("capital", "behavior", "influence", "network", "historical", "cross_chain", "confidence")

    def score(self, classifications: tuple[LabelType, ...], metrics: Metrics) -> WhaleScoreSet:
        values = dict(metrics)
        normalized = {name: max(0.0, min(100.0, float(values.get(name, 0.0)))) for name in self.DIMENSIONS}
        return WhaleScoreSet(
            CapitalScore(normalized["capital"]),
            BehaviorScore(normalized["behavior"]),
            InfluenceScore(normalized["influence"]),
            NetworkScore(normalized["network"]),
            HistoricalScore(normalized["historical"]),
            CrossChainScore(normalized["cross_chain"]),
            ConfidenceScore(normalized["confidence"]),
        )
