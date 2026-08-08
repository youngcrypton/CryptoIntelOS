from typing import Protocol

from .evidence_bundle import UnifiedEvidenceBundle
from .fusion_context import FusionContext
from .fusion_result import FusionResult
from src.core_intelligence.models import Evidence
from src.unified_intelligence.entity_linking import IdentityBundle


class EvidenceFusionStrategy(Protocol):
    strategy_id: str

    def fuse(self, identity: IdentityBundle, evidence: tuple[Evidence, ...], context: FusionContext) -> FusionResult: ...
