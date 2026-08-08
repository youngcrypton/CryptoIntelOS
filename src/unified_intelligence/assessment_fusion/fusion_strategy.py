from typing import Protocol

from src.core_intelligence.models import Assessment
from src.unified_intelligence.entity_linking import IdentityBundle
from src.unified_intelligence.evidence_fusion import UnifiedEvidenceBundle
from src.unified_intelligence.finding_fusion import ProjectFindingGroup

from .fusion_context import AssessmentFusionContext
from .fusion_result import AssessmentFusionResult


class AssessmentFusionStrategy(Protocol):
    strategy_id: str

    def fuse(self, identity: IdentityBundle, evidence: UnifiedEvidenceBundle, findings: ProjectFindingGroup, assessments: tuple[Assessment, ...], context: AssessmentFusionContext) -> AssessmentFusionResult: ...
