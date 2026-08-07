from typing import Protocol
from .reasoning_context import ReasoningContext
from .reasoning_request import ReasoningRequest
from .reasoning_result import ReasoningResult
class ReasoningStrategy(Protocol):
    def execute(self, request: ReasoningRequest, context: ReasoningContext) -> ReasoningResult: ...
