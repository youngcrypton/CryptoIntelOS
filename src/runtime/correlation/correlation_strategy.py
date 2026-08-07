from typing import Protocol
from .correlation_context import CorrelationContext
from .correlation_result import CorrelationResult
class CorrelationStrategy(Protocol):
    def correlate(self, objects: tuple[object, ...], context: CorrelationContext) -> CorrelationResult: ...
