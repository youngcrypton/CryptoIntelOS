from dataclasses import dataclass
from .correlation_context import CorrelationContext
from .correlation_result import CorrelationResult
from .correlation_strategy import CorrelationStrategy
@dataclass(slots=True)
class CorrelationEngine:
    def correlate(self, strategy: CorrelationStrategy, objects: tuple[object, ...], context: CorrelationContext) -> CorrelationResult:
        return strategy.correlate(objects, context)
