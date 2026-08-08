from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssessmentFusionConfidence:
    value: float
    rationale: str
