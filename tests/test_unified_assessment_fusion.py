from datetime import UTC, datetime

from src.core_intelligence.identity import Entity, EntityType, Identifier, IdentifierType, Identity
from src.core_intelligence.models import Assessment, Evidence, Finding
from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.unified_intelligence.assessment_fusion import ASSESSMENT_CATEGORIES, AssessmentFusionContext, AssessmentFusionEngine, AssessmentFusionStrategy, DeterministicAssessmentFusion, FusionRegistry, ProjectAssessment
from src.unified_intelligence.entity_linking import EntityCandidate, EntityLinker, LinkingContext
from src.unified_intelligence.evidence_fusion import EvidenceFusionEngine, FusionContext
from src.unified_intelligence.finding_fusion import FindingFusionContext, FindingFusionEngine


NOW = datetime(2026, 8, 8, tzinfo=UTC)


def inputs():
    identifier = Identifier("example.org", IdentifierType.WEBSITE_DOMAIN)
    candidate = EntityCandidate("website", Entity(entity_type=EntityType.PROJECT, identity=Identity("Example", (identifier,))), "Example", (identifier,))
    identity = EntityLinker().link((candidate,), LinkingContext("execution-1")).bundle
    canonical_evidence = (Evidence("web-1", "project:example", "obs-1", "security", True, .9, "website", {"url": "example.org/audit"}, NOW),)
    evidence = EvidenceFusionEngine().fuse(identity, canonical_evidence, FusionContext("execution-1", identity.canonical_project_identifier)).bundle
    canonical_findings = (Finding("finding-1", "project:example", "Security Focus", .9, ("web-1",), "Audit evidence", NOW),)
    findings = FindingFusionEngine().fuse(identity, evidence, canonical_findings, FindingFusionContext("execution-1", identity.canonical_project_identifier)).group
    assessments = (Assessment("assessment-1", "project:example", "Security Readiness", 90, .9, ("web-1",), "website-policy", "1.0", NOW),)
    return identity, evidence, findings, assessments


def test_project_assessment_preserves_findings_evidence_and_provenance():
    identity, evidence, findings, assessments = inputs()
    result = AssessmentFusionEngine().fuse(identity, evidence, findings, assessments, AssessmentFusionContext("execution-1", identity.canonical_project_identifier))
    project = result.group.assessments[0]
    assert isinstance(project, ProjectAssessment)
    assert project.category == "Security Readiness"
    assert project.supporting_findings == ("finding-1",)
    assert project.supporting_evidence == ("web-1",)
    assert project.provenance == (("assessment-1", "website"),)
    assert project.confidence.value == .9
    assert "Security Readiness" in ASSESSMENT_CATEGORIES


def test_strategy_registry_and_runtime_delegation():
    registry = FusionRegistry()
    strategy = DeterministicAssessmentFusion()
    registry.register(strategy)
    assert registry.get(strategy.strategy_id) is strategy
    assert "fuse" in AssessmentFusionStrategy.__dict__
    identity, evidence, findings, assessments = inputs()
    group = AssessmentFusionEngine().fuse(identity, evidence, findings, assessments, AssessmentFusionContext("execution-1", identity.canonical_project_identifier)).group
    context = ExecutionContext("execution-1", "1.0", NOW)
    calls = []
    def entrypoint(value, supplied):
        calls.append((value, supplied))
        return ExecutionResult(supplied.execution_id, ExecutionState.COMPLETED)
    result = AssessmentFusionEngine.enter_runtime(group, RuntimeFacade(entrypoint), context)
    assert result.final_state is ExecutionState.COMPLETED
    assert calls == [(group, context)]
