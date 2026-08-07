from dataclasses import dataclass
from .reasoning_explanation import ReasoningExplanation
@dataclass(frozen=True, slots=True)
class ReasoningStep:
    step_id: str
    description: str
    input_references: tuple[str, ...] = ()
    output: str | None = None
    explanation: ReasoningExplanation | None = None
