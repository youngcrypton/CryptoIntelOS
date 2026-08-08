from typing import Protocol

from src.core_intelligence.models import Signal
from src.unified_intelligence.assessment_fusion import ProjectAssessmentGroup
from src.unified_intelligence.entity_linking import IdentityBundle
from src.unified_intelligence.evidence_fusion import UnifiedEvidenceBundle
from src.unified_intelligence.finding_fusion import ProjectFindingGroup

from .profile_context import ProfileContext
from .profile_metadata import ProfileMetadata
from .profile_result import ProfileResult


class ProfileStrategy(Protocol):
    strategy_id: str

    def build(self, identity: IdentityBundle, evidence: UnifiedEvidenceBundle, findings: ProjectFindingGroup, assessments: ProjectAssessmentGroup, signals: tuple[Signal, ...], metadata: ProfileMetadata, context: ProfileContext) -> ProfileResult: ...
