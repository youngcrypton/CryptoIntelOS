from typing import Protocol
from .reasoning_context import ReasoningContext
from .reasoning_prompt import ReasoningPrompt
from .reasoning_request import ReasoningRequest
from .reasoning_result import ReasoningResult
class ReasoningProvider(Protocol):
    def reason(self, request: ReasoningRequest, prompt: ReasoningPrompt, context: ReasoningContext) -> ReasoningResult: ...
