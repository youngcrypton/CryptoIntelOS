from dataclasses import dataclass

from src.unified_intelligence.entity_linking import IdentityBundle

from .confidence import FindingFusionConfidence
from .finding_reference import FindingReference
from .finding_trace import FindingTrace


@dataclass(frozen=True, slots=True)
class ProjectFinding:
    identity: IdentityBundle
    finding_category: str
    supporting_findings: tuple[FindingReference, ...]
    supporting_evidence: tuple[str, ...]
    provenance: tuple[tuple[str, str], ...]
    traceability: tuple[FindingTrace, ...]
    confidence: FindingFusionConfidence
