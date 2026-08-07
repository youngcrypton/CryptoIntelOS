"""Declarative contract describing a pluggable resolution strategy."""
from dataclasses import dataclass
from enum import StrEnum

class ResolutionStrategyType(StrEnum):
    EXACT_MATCH = "exact_match"
    IDENTIFIER_MATCH = "identifier_match"
    EVIDENCE_MATCH = "evidence_match"
    AI_ASSISTED = "ai_assisted"
    GRAPH_ASSISTED = "graph_assisted"

@dataclass(frozen=True, slots=True)
class ResolutionStrategy:
    name: str
    strategy_type: ResolutionStrategyType
    version: str = "1"
