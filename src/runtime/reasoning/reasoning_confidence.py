from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class ReasoningConfidence:
    confidence: float
    confidence_source: str
    supporting_evidence: tuple[str, ...] = ()
    uncertainty: float | None = None
    explanation: str | None = None
