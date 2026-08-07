from dataclasses import dataclass
from .correlation import Correlation
from .correlation_status import CorrelationStatus
@dataclass(frozen=True, slots=True)
class CorrelationResult:
    status: CorrelationStatus
    correlations: tuple[Correlation, ...] = ()
    metadata: tuple[tuple[str,str], ...] = ()
