from dataclasses import dataclass

from src.unified_intelligence.entity_linking import IdentityBundle

from .assessment_reference import AssessmentReference
from .assessment_trace import AssessmentTrace
from .confidence import AssessmentFusionConfidence


@dataclass(frozen=True, slots=True)
class ProjectAssessment:
    identity: IdentityBundle
    category: str
    score: float
    supporting_assessments: tuple[AssessmentReference, ...]
    supporting_findings: tuple[str, ...]
    supporting_evidence: tuple[str, ...]
    provenance: tuple[tuple[str, str], ...]
    traceability: tuple[AssessmentTrace, ...]
    confidence: AssessmentFusionConfidence
