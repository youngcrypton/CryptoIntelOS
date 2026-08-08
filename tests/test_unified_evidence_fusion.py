from datetime import UTC, datetime

from src.core_intelligence.identity import Entity, EntityType, Identifier, IdentifierType, Identity
from src.core_intelligence.models import Evidence
from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.unified_intelligence.entity_linking import EntityCandidate, EntityLinker, LinkingContext
from src.unified_intelligence.evidence_fusion import DeterministicEvidenceFusion, EvidenceFusionEngine, EvidenceFusionStrategy, FusionContext, FusionRegistry, UnifiedEvidenceBundle


def identity():
    candidate = EntityCandidate("website", Entity(entity_type=EntityType.PROJECT, identity=Identity(canonical_name="Example", identifiers=(Identifier("example.org", IdentifierType.WEBSITE_DOMAIN),))), "Example", (Identifier("example.org", IdentifierType.WEBSITE_DOMAIN),))
    return EntityLinker().link((candidate,), LinkingContext("execution-1")).bundle


def evidence(evidence_id, source, metric, timestamp):
    return Evidence(evidence_id, "project:example", "obs-1", metric, {"value": evidence_id}, .9, source, {"origin": source}, timestamp)


def test_fusion_groups_and_preserves_provenance():
    timestamp = datetime(2026, 8, 8, tzinfo=UTC)
    result = EvidenceFusionEngine().fuse(identity(), (evidence("web-1", "website", "official", timestamp), evidence("gh-1", "github", "repository", timestamp), evidence("web-2", "website", "official", timestamp)), FusionContext("execution-1", "project:example"))
    bundle = result.bundle
    assert isinstance(bundle, UnifiedEvidenceBundle)
    assert len(bundle.groups) == 2
    assert bundle.source_map[0][1]
    assert set(bundle.traceability) == {"web-1", "web-2", "gh-1"}
    assert bundle.groups[1].traces[0].origin == "obs-1"


def test_strategy_registry_and_runtime_delegation():
    registry = FusionRegistry()
    strategy = DeterministicEvidenceFusion()
    registry.register(strategy)
    assert registry.get(strategy.strategy_id) is strategy
    assert "fuse" in EvidenceFusionStrategy.__dict__
    bundle = EvidenceFusionEngine().fuse(identity(), (), FusionContext("execution-1", "project:example")).bundle
    context = ExecutionContext("execution-1", "1.0", datetime(2026, 8, 8, tzinfo=UTC))
    calls = []
    def entrypoint(value, supplied):
        calls.append((value, supplied))
        return ExecutionResult(supplied.execution_id, ExecutionState.COMPLETED)
    from src.unified_intelligence.runtime import UnifiedRuntimeIntegration
    result = UnifiedRuntimeIntegration(RuntimeFacade(entrypoint)).integrate(bundle, context)
    assert result.final_state is ExecutionState.COMPLETED
    assert calls == [(bundle, context)]
