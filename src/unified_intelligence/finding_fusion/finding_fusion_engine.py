from collections import defaultdict

from src.core_intelligence.models import Finding
from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult
from src.unified_intelligence.entity_linking import IdentityBundle
from src.unified_intelligence.evidence_fusion import UnifiedEvidenceBundle

from .confidence import FindingFusionConfidence
from .finding_group import ProjectFindingGroup
from .finding_reference import FindingReference
from .finding_trace import FindingTrace
from .fusion_context import FindingFusionContext
from .fusion_registry import FusionRegistry
from .fusion_result import FindingFusionResult
from .project_finding import ProjectFinding


class DeterministicFindingFusion:
    strategy_id = "deterministic-finding-v1"

    def fuse(self, identity: IdentityBundle, evidence: UnifiedEvidenceBundle, findings: tuple[Finding, ...], context: FindingFusionContext) -> FindingFusionResult:
        evidence_sources = {reference.evidence_id: reference.source for group in evidence.groups for reference in group.references}
        grouped: dict[tuple[str, str, tuple[str, ...]], list[Finding]] = defaultdict(list)
        for finding in findings:
            key = (identity.canonical_project_identifier, finding.finding_type, tuple(sorted(finding.supporting_evidence)))
            grouped[key].append(finding)
        project_findings = []
        for (identity_id, category, evidence_ids), items in sorted(grouped.items()):
            sources = tuple(sorted({evidence_sources.get(evidence_id, "unknown") for evidence_id in evidence_ids}))
            references = tuple(FindingReference(item.finding_id, self._source(item, evidence_sources), item) for item in items)
            trace_key = f"{identity_id}:{category}:{','.join(evidence_ids)}"
            traces = tuple(FindingTrace(item.finding_id, self._source(item, evidence_sources), item.supporting_evidence, trace_key) for item in items)
            confidence = round(sum(item.confidence for item in items) / len(items), 4)
            project_findings.append(ProjectFinding(identity, category, references, evidence_ids, tuple((item.finding_id, self._source(item, evidence_sources)) for item in items), traces, FindingFusionConfidence(confidence, "mean of originating canonical finding confidence")))
        return FindingFusionResult(ProjectFindingGroup(identity.canonical_project_identifier, tuple(project_findings)))

    @staticmethod
    def _source(finding: Finding, evidence_sources: dict[str, str]) -> str:
        return next((evidence_sources[item] for item in finding.supporting_evidence if item in evidence_sources), "unknown")


class FindingFusionEngine:
    def __init__(self, registry: FusionRegistry | None = None) -> None:
        self.registry = registry or self.default_registry()

    @staticmethod
    def default_registry() -> FusionRegistry:
        registry = FusionRegistry()
        registry.register(DeterministicFindingFusion())
        return registry

    def fuse(self, identity: IdentityBundle, evidence: UnifiedEvidenceBundle, findings: tuple[Finding, ...], context: FindingFusionContext) -> FindingFusionResult:
        return self.registry.get("deterministic-finding-v1").fuse(identity, evidence, findings, context)

    @staticmethod
    def enter_runtime(group: ProjectFindingGroup, facade: RuntimeFacade, context: ExecutionContext) -> ExecutionResult:
        from src.unified_intelligence.runtime_projection import project_finding_group

        return facade.integrate(project_finding_group(group, context), context)
