from dataclasses import dataclass

from src.core_intelligence.models import Signal
from src.unified_intelligence.assessment_fusion import ProjectAssessmentGroup
from src.unified_intelligence.entity_linking import IdentityBundle
from src.unified_intelligence.evidence_fusion import UnifiedEvidenceBundle
from src.unified_intelligence.finding_fusion import ProjectFindingGroup

from .profile_context import ProfileContext
from .profile_metadata import ProfileMetadata


@dataclass(frozen=True, slots=True)
class ProjectIntelligenceProfile:
    canonical_project_identifier: str
    identity_bundle: IdentityBundle
    unified_evidence: UnifiedEvidenceBundle
    unified_findings: ProjectFindingGroup
    unified_assessments: ProjectAssessmentGroup
    canonical_signals: tuple[Signal, ...]
    relationships: tuple[tuple[str, str], ...]
    provenance: tuple[tuple[str, str], ...]
    traceability: tuple[str, ...]
    confidence: float
    runtime_metadata: ProfileMetadata
    execution_metadata: ProfileContext
