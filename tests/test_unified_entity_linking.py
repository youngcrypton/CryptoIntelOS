from datetime import UTC, datetime

from src.core_intelligence.identity import Entity, EntityType, Identifier, IdentifierType, Identity
from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.unified_intelligence import (
    DeterministicEntityResolution, EntityCandidate, EntityLinker, EntityLinkingStrategy, IdentityBundle, LinkingContext, LinkingRegistry, UnifiedRuntimeIntegration,
)


def candidate(source, name, identifiers):
    entity = Entity(entity_type=EntityType.PROJECT, identity=Identity(canonical_name=name, identifiers=tuple(identifiers)))
    return EntityCandidate(source, entity, name, tuple(identifiers), (f"{source}:official",))


def test_deterministic_linking_uses_exact_identifiers():
    website = candidate("website", "Example", (Identifier("example.org", IdentifierType.WEBSITE_DOMAIN),))
    github = candidate("github", "Other", (Identifier("example.org", IdentifierType.WEBSITE_DOMAIN), Identifier("repo-1", IdentifierType.GITHUB_REPOSITORY_ID)))
    result = EntityLinker().link((website, github), LinkingContext("execution-1"))
    assert result.matches[0].matched_identifiers == ("example.org",)
    assert result.bundle.canonical_project_identifier == "project:example"
    assert result.bundle.github_references[0].value == "repo-1"
    assert result.bundle.supporting_evidence


def test_candidate_bundle_and_confidence_are_immutable():
    website = candidate("website", "Example", (Identifier("example.org", IdentifierType.WEBSITE_DOMAIN),))
    bundle = EntityLinker().link((website,), LinkingContext("execution-1")).bundle
    assert isinstance(bundle, IdentityBundle)
    assert bundle.confidence.value == .5
    try:
        bundle.canonical_project_identifier = "changed"
    except AttributeError:
        return
    raise AssertionError("IdentityBundle was mutable")


def test_strategy_registry_and_runtime_delegation():
    registry = LinkingRegistry()
    strategy = DeterministicEntityResolution()
    registry.register(strategy)
    assert registry.get(strategy.strategy_id) is strategy
    assert "link" in EntityLinkingStrategy.__dict__
    bundle = EntityLinker().link((candidate("website", "Example", ()),), LinkingContext("execution-1")).bundle
    now = datetime(2026, 8, 8, tzinfo=UTC)
    context = ExecutionContext("execution-1", "1.0", now)
    received = []
    def entrypoint(value, supplied):
        received.append((value, supplied))
        return ExecutionResult(supplied.execution_id, ExecutionState.COMPLETED)
    result = UnifiedRuntimeIntegration(RuntimeFacade(entrypoint)).integrate(bundle, context)
    assert result.final_state is ExecutionState.COMPLETED
    assert received == [(bundle, context)]
