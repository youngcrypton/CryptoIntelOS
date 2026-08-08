from typing import Protocol

from src.core_intelligence.models import Finding
from src.unified_intelligence.entity_linking import IdentityBundle
from src.unified_intelligence.evidence_fusion import UnifiedEvidenceBundle

from .fusion_context import FindingFusionContext
from .fusion_result import FindingFusionResult


class FindingFusionStrategy(Protocol):
    strategy_id: str

    def fuse(self, identity: IdentityBundle, evidence: UnifiedEvidenceBundle, findings: tuple[Finding, ...], context: FindingFusionContext) -> FindingFusionResult: ...
