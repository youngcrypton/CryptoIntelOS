from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WhaleAssessment:
    dimension: str
    score: float
    confidence: float
    evidence: tuple[str, ...]
    explanation: str
