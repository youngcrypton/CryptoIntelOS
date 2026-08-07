from dataclasses import dataclass

from .confidence import LinkingConfidence
from .entity_candidate import EntityCandidate


@dataclass(frozen=True, slots=True)
class EntityMatch:
    left: EntityCandidate
    right: EntityCandidate
    matched_identifiers: tuple[str, ...]
    confidence: LinkingConfidence
    explanation: str
