from datetime import UTC, datetime
from io import StringIO

from src.core_intelligence.identity import Entity, EntityType, Identifier, IdentifierType, Identity
from src.core_intelligence.models import Assessment, Evidence, Finding, Signal
from src.runtime.correlation import CorrelationStatus
from src.runtime.engine import ExecutionState
from src.unified_intelligence.entity_linking import EntityCandidate
from src.unified_intelligence.profile import ProjectIntelligenceProfile, SourceIntelligence, UnifiedIntelligenceVerticalSlice


NOW = datetime(2026, 8, 8, tzinfo=UTC)


def source(name, extra_identifier, evidence_id, finding_id, assessment_id, signal_id):
    domain = Identifier("example.org", IdentifierType.WEBSITE_DOMAIN)
    candidate = EntityCandidate(name, Entity(entity_type=EntityType.PROJECT, identity=Identity("Example", (domain, extra_identifier))), "Example", (domain, extra_identifier))
    evidence = Evidence(evidence_id, "project:example", f"{name}:observation", f"{name}.activity", True, .9, name, {"source": name}, NOW)
    finding = Finding(finding_id, "project:example", f"{name.title()} Activity", .9, (evidence_id,), f"{name} activity confirmed", NOW)
    assessment = Assessment(assessment_id, "project:example", "Adoption Momentum", 90, .9, (evidence_id,), f"{name}-policy", "1.0", NOW)
    signal = Signal(signal_id, "project:example", f"{name.title()} Signal", "medium", .9, "Monitor", "Canonical source signal", (evidence_id,), NOW)
    return SourceIntelligence(name, candidate, (evidence,), (finding,), (assessment,), (signal,))


def test_complete_unified_intelligence_vertical_slice():
    sources = (
        source("github", Identifier("repo-1", IdentifierType.GITHUB_REPOSITORY_ID), "gh-e", "gh-f", "gh-a", "gh-s"),
        source("twitter", Identifier("example", IdentifierType.TWITTER_USERNAME), "tw-e", "tw-f", "tw-a", "tw-s"),
        source("website", Identifier("https://example.org", IdentifierType.URL), "web-e", "web-f", "web-a", "web-s"),
        source("wallet", Identifier("wallet-1", IdentifierType.WALLET_ADDRESS), "wal-e", "wal-f", "wal-a", "wal-s"),
    )
    console = StringIO()
    result = UnifiedIntelligenceVerticalSlice().run(sources, output=console)
    assert isinstance(result.profile, ProjectIntelligenceProfile)
    assert result.profile.canonical_project_identifier == "project:example"
    assert len(result.profile.identity_bundle.traceability) == 4
    assert len(result.profile.unified_evidence.traceability) == 4
    assert len(result.profile.unified_findings.findings) == 4
    assert len(result.profile.unified_assessments.assessments) == 4
    assert len(result.profile.canonical_signals) == 4
    assert result.runtime.compilation.projection.nodes
    assert len(result.runtime.graph.nodes) == len(result.runtime.compilation.projection.nodes)
    assert result.runtime.correlation.status is CorrelationStatus.CONFIRMED
    assert result.runtime.reasoning.status.value == "completed"
    assert result.runtime.automation.actions
    assert result.runtime.distribution.requests
    assert result.runtime.execution.final_state is ExecutionState.COMPLETED
    for phrase in ("Project Identified", "Sources Linked", "Evidence Items", "Project Findings", "Project Assessments", "Signals", "Compiler Executed", "Knowledge Graph Updated", "Correlation Completed", "Reasoning Completed", "Automation Planned", "Distribution Planned", "Execution Successful"):
        assert phrase in console.getvalue()
