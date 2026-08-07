from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class ReasoningExplanation:
    summary: str
    evidence_references: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    limitations: tuple[str, ...] = ()
