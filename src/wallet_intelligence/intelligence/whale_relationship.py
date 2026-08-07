from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WhaleRelationship:
    source_wallet: str
    target_reference: str
    relationship_type: str
    confidence: float
    evidence: tuple[str, ...] = ()
