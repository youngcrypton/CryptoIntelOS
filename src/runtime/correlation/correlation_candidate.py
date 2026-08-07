from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .correlation import Correlation
@dataclass(frozen=True, slots=True)
class CorrelationCandidate:
    correlation: Correlation
    candidate_id: UUID = field(default_factory=uuid4)
    confidence: float | None = None
    explanation: str | None = None
