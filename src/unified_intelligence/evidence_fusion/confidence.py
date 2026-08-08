from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FusionConfidence:
    value: float
    rationale: str
