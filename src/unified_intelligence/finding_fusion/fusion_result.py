from dataclasses import dataclass

from .finding_group import ProjectFindingGroup


@dataclass(frozen=True, slots=True)
class FindingFusionResult:
    group: ProjectFindingGroup
