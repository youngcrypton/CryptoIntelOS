from dataclasses import dataclass
from .reasoning_chain import ReasoningChain
from .reasoning_confidence import ReasoningConfidence
from .reasoning_explanation import ReasoningExplanation
from .reasoning_status import ReasoningStatus
@dataclass(frozen=True, slots=True)
class ReasoningResult:
    status: ReasoningStatus
    conclusion: str | None = None
    chain: ReasoningChain | None = None
    confidence: ReasoningConfidence | None = None
    explanation: ReasoningExplanation | None = None
    provenance: tuple[str, ...] = ()
