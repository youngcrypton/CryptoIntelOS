from dataclasses import dataclass

from src.core_intelligence.models import Assessment


@dataclass(frozen=True, slots=True)
class AssessmentReference:
    assessment_id: str
    source: str
    assessment: Assessment
