from dataclasses import dataclass
from .reasoning_step import ReasoningStep
@dataclass(frozen=True, slots=True)
class ReasoningChain:
    steps: tuple[ReasoningStep, ...] = ()
    strategy: str | None = None
