from dataclasses import dataclass
from .correlation_candidate import CorrelationCandidate
@dataclass(frozen=True, slots=True)
class CorrelationGroup:
    candidates: tuple[CorrelationCandidate, ...] = ()
    group_reference: str | None = None
