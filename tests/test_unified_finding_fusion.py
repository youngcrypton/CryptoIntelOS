from datetime import UTC, datetime

from src.core_intelligence.identity import Entity, EntityType, Identifier, IdentifierType, Identity
from src.core_intelligence.models import Evidence, Finding
from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.unified_intelligence.entity_linking import EntityCandidate, EntityLinker, LinkingContext
from src.unified_intelligence.evidence_fusion import EvidenceFusionEngine, FusionContext
from src.unified_intelligence.finding_fusion import DeterministicFindingFusion, FindingFusionContext, FindingFusionEngine, FindingFusionStrategy, FusionRegistry, ProjectFinding


NOW = datetime(2026, 8, 8, tzinfo=UTC)


def inputs():
    identifier = Identifier("example.org", IdentifierType.WEBSITE_DOMAIN)
    candidate = EntityCandidate("website", Entity(entity_type=EntityType.PROJECT, identity=Identity("Example", (identifier,))), "Example", (identifier,))
    identity = EntityLinker().link((candidate,), LinkingContext("execution-1")).bundle
    evidence = (Evidence("web-1", "project:example", "obs-1", "documentation", True, .9, "website", {"url": "example.org/docs"}, NOW), Evidence("gh-1", "project:example", "obs-2", "activity", 10, .8, "github", {"repository": "repo-1"}, NOW))
    bundle = EvidenceFusionEngine().fuse(identity, evidence, FusionContext("execution-1", identity.canonical_project_identifier)).bundle
    findings = (Finding("finding-1", "project:example", "Project Activity", .8, ("gh-1",), "Repository activity confirmed", NOW), Finding("finding-2", "project:example", "Documentation Quality", .9, ("web-1",), "Documentation confirmed", NOW))
    return identity, bundle, findings


def test_project_finding_group_preserves_evidence_and_traceability():
    identity, evidence, findings = inputs()
    result = FindingFusionEngine().fuse(identity, evidence, findings, FindingFusionContext("execution-1", identity.canonical_project_identifier))
    assert len(result.group.findings) == 2
    assert all(isinstance(item, ProjectFinding) for item in result.group.findings)
    documentation = next(item for item in result.group.findings if item.finding_category == "Documentation Quality")
    assert documentation.supporting_evidence == ("web-1",)
    assert documentation.provenance == (("finding-2", "website"),)
    assert documentation.traceability[0].finding_id == "finding-2"
    assert documentation.confidence.value == .9


def test_strategy_registry_and_runtime_delegation():
    registry = FusionRegistry()
    strategy = DeterministicFindingFusion()
    registry.register(strategy)
    assert registry.get(strategy.strategy_id) is strategy
    assert "fuse" in FindingFusionStrategy.__dict__
    identity, evidence, findings = inputs()
    group = FindingFusionEngine().fuse(identity, evidence, findings, FindingFusionContext("execution-1", identity.canonical_project_identifier)).group
    context = ExecutionContext("execution-1", "1.0", NOW)
    calls = []
    def entrypoint(value, supplied):
        calls.append((value, supplied))
        return ExecutionResult(supplied.execution_id, ExecutionState.COMPLETED)
    result = FindingFusionEngine.enter_runtime(group, RuntimeFacade(entrypoint), context)
    assert result.final_state is ExecutionState.COMPLETED
    assert calls == [(group, context)]
