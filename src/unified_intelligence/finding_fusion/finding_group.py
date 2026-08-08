from dataclasses import dataclass

from .project_finding import ProjectFinding


@dataclass(frozen=True, slots=True)
class ProjectFindingGroup:
    identity_identifier: str
    findings: tuple[ProjectFinding, ...]
