from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CapitalScore:
    value: float


@dataclass(frozen=True, slots=True)
class BehaviorScore:
    value: float


@dataclass(frozen=True, slots=True)
class InfluenceScore:
    value: float


@dataclass(frozen=True, slots=True)
class NetworkScore:
    value: float


@dataclass(frozen=True, slots=True)
class HistoricalScore:
    value: float


@dataclass(frozen=True, slots=True)
class CrossChainScore:
    value: float


@dataclass(frozen=True, slots=True)
class ConfidenceScore:
    value: float


@dataclass(frozen=True, slots=True)
class WhaleScoreSet:
    capital: CapitalScore
    behavior: BehaviorScore
    influence: InfluenceScore
    network: NetworkScore
    historical: HistoricalScore
    cross_chain: CrossChainScore
    confidence: ConfidenceScore
