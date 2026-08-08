from dataclasses import dataclass

from .project_assessment import ProjectAssessment


@dataclass(frozen=True, slots=True)
class ProjectAssessmentGroup:
    identity_identifier: str
    assessments: tuple[ProjectAssessment, ...]
