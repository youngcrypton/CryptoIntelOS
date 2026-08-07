from dataclasses import dataclass

from src.wallet_intelligence import LabelType

from .scoring_strategy import Metrics
from .whale_category import WhaleCategory
from .whale_evidence import WhaleEvidence
from .whale_relationship import WhaleRelationship
from .whale_score import WhaleScoreSet


@dataclass(frozen=True, slots=True)
class WhaleProfile:
    canonical_identifier: str
    wallet_references: tuple[str, ...]
    classification: tuple[LabelType, ...]
    categories: tuple[WhaleCategory, ...]
    capital_metrics: Metrics
    behavior_metrics: Metrics
    influence_metrics: Metrics
    network_metrics: Metrics
    historical_performance_metrics: Metrics
    cross_chain_activity_metrics: Metrics
    scores: WhaleScoreSet
    confidence: float
    supporting_evidence: tuple[WhaleEvidence, ...]
    relationships: tuple[WhaleRelationship, ...] = ()
