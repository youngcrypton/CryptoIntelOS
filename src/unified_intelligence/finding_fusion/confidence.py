from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FindingFusionConfidence:
    value: float
    rationale: str
