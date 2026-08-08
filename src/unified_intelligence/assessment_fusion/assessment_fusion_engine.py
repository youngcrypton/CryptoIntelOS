from collections import defaultdict

from src.core_intelligence.models import Assessment
from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult
from src.unified_intelligence.entity_linking import IdentityBundle
from src.unified_intelligence.evidence_fusion import UnifiedEvidenceBundle
from src.unified_intelligence.finding_fusion import ProjectFindingGroup

from .assessment_group import ProjectAssessmentGroup
from .assessment_reference import AssessmentReference
from .assessment_trace import AssessmentTrace
from .confidence import AssessmentFusionConfidence
from .fusion_context import AssessmentFusionContext
from .fusion_registry import FusionRegistry
from .fusion_result import AssessmentFusionResult
from .project_assessment import ProjectAssessment


ASSESSMENT_CATEGORIES = (
    "Engineering Maturity", "Community Health", "Treasury Strength", "Product Maturity",
    "Execution Velocity", "Security Readiness", "Governance Quality", "Adoption Momentum",
    "Operational Risk", "Market Confidence",
)


class DeterministicAssessmentFusion:
    strategy_id = "deterministic-assessment-v1"

    def fuse(self, identity: IdentityBundle, evidence: UnifiedEvidenceBundle, findings: ProjectFindingGroup, assessments: tuple[Assessment, ...], context: AssessmentFusionContext) -> AssessmentFusionResult:
        evidence_sources = {reference.evidence_id: reference.source for group in evidence.groups for reference in group.references}
        finding_map = {reference.finding_id: item for item in findings.findings for reference in item.supporting_findings}
        grouped: dict[tuple[str, str, tuple[str, ...], tuple[str, ...]], list[Assessment]] = defaultdict(list)
        for assessment in assessments:
            category = assessment.assessment_type
            evidence_ids = tuple(sorted(assessment.evidence))
            finding_ids = tuple(sorted(finding_id for finding_id, project_finding in finding_map.items() if set(project_finding.supporting_evidence) & set(evidence_ids)))
            grouped[(identity.canonical_project_identifier, category, finding_ids, evidence_ids)].append(assessment)
        project_assessments = []
        for (identity_id, category, finding_ids, evidence_ids), items in sorted(grouped.items()):
            references = tuple(AssessmentReference(item.assessment_id, self._source(item, evidence_sources), item) for item in items)
            trace_key = f"{identity_id}:{category}:{','.join(finding_ids)}:{','.join(evidence_ids)}"
            traces = tuple(AssessmentTrace(item.assessment_id, self._source(item, evidence_sources), finding_ids, item.evidence, trace_key) for item in items)
            score = round(sum(item.score for item in items) / len(items), 4)
            confidence = round(sum(item.confidence for item in items) / len(items), 4)
            provenance = tuple((item.assessment_id, self._source(item, evidence_sources)) for item in items)
            project_assessments.append(ProjectAssessment(identity, category, score, references, finding_ids, evidence_ids, provenance, traces, AssessmentFusionConfidence(confidence, "mean of originating canonical assessment confidence")))
        return AssessmentFusionResult(ProjectAssessmentGroup(identity.canonical_project_identifier, tuple(project_assessments)))

    @staticmethod
    def _source(assessment: Assessment, evidence_sources: dict[str, str]) -> str:
        return next((evidence_sources[item] for item in assessment.evidence if item in evidence_sources), "unknown")


class AssessmentFusionEngine:
    def __init__(self, registry: FusionRegistry | None = None) -> None:
        self.registry = registry or self.default_registry()

    @staticmethod
    def default_registry() -> FusionRegistry:
        registry = FusionRegistry()
        registry.register(DeterministicAssessmentFusion())
        return registry

    def fuse(self, identity: IdentityBundle, evidence: UnifiedEvidenceBundle, findings: ProjectFindingGroup, assessments: tuple[Assessment, ...], context: AssessmentFusionContext) -> AssessmentFusionResult:
        return self.registry.get("deterministic-assessment-v1").fuse(identity, evidence, findings, assessments, context)

    @staticmethod
    def enter_runtime(group: ProjectAssessmentGroup, facade: RuntimeFacade, context: ExecutionContext) -> ExecutionResult:
        return facade.integrate(group, context)  # type: ignore[arg-type]
