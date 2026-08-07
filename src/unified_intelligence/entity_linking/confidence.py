from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LinkingConfidence:
    value: float
    rationale: str
