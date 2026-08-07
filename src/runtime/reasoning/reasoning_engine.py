from dataclasses import dataclass
from .reasoning_context import ReasoningContext
from .reasoning_request import ReasoningRequest
from .reasoning_result import ReasoningResult
from .reasoning_strategy import ReasoningStrategy
@dataclass(slots=True)
class ReasoningEngine:
    def reason(self, strategy: ReasoningStrategy, request: ReasoningRequest, context: ReasoningContext) -> ReasoningResult:
        return strategy.execute(request, context)
