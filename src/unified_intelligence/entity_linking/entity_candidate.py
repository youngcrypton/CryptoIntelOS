from dataclasses import dataclass

from src.core_intelligence.identity import Entity, Identifier


@dataclass(frozen=True, slots=True)
class EntityCandidate:
    source: str
    entity: Entity
    canonical_name: str
    identifiers: tuple[Identifier, ...] = ()
    evidence: tuple[str, ...] = ()
