from dataclasses import dataclass

from .assessment_group import ProjectAssessmentGroup


@dataclass(frozen=True, slots=True)
class AssessmentFusionResult:
    group: ProjectAssessmentGroup
