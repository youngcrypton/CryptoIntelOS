from datetime import UTC, datetime

from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.website_intelligence import (
    Document,
    Link,
    Page,
    Website,
    WebsiteAnalysisEngine,
    WebsiteDiscoveryEngine,
    WebsiteRuntimeIntegration,
)


NOW = datetime(2026, 8, 7, tzinfo=UTC)


def analyze(value):
    discovery = WebsiteDiscoveryEngine()
    if isinstance(value, Website):
        observation = discovery.discover_website(value).observation
    elif isinstance(value, Page):
        observation = discovery.discover_page(value).observation
    elif isinstance(value, Document):
        observation = discovery.discover_document(value).observation
    else:
        observation = discovery.discover_link(value).observation
    return WebsiteAnalysisEngine().analyze(observation)


def finding_types(output) -> set[str]:
    return {item.finding_type for item in output.findings}


def assessment_types(output) -> set[str]:
    return {item.assessment_type for item in output.assessments}


def test_identity_analysis() -> None:
    output = analyze(Website("site-1", "https://example.org", "example.org", "Example"))
    assert "Verified Official Website" in finding_types(output)
    assert "Identity Confidence" in assessment_types(output)


def test_documentation_analysis() -> None:
    output = analyze(Document("doc-1", "site-1", "https://example.org/docs", "documentation"))
    assert "Strong Documentation" in finding_types(output)
    assert "Documentation Quality" in assessment_types(output)


def test_roadmap_analysis() -> None:
    output = analyze(Page("page-1", "site-1", "https://example.org/roadmap", "Roadmap"))
    assert "Public Roadmap" in finding_types(output)


def test_team_analysis() -> None:
    output = analyze(Page("page-1", "site-1", "https://example.org/team", "Team"))
    assert "Transparent Team" in finding_types(output)
    assert "Team Transparency" in assessment_types(output)


def test_careers_analysis() -> None:
    output = analyze(Page("page-1", "site-1", "https://example.org/careers", "We're hiring"))
    assert "Active Hiring" in finding_types(output)
    assert "Hiring Activity" in assessment_types(output)


def test_audit_analysis() -> None:
    output = analyze(Page("page-1", "site-1", "https://example.org/audits", "Security Audits"))
    assert "Security Focus" in finding_types(output)
    assert "Security Maturity" in assessment_types(output)


def test_ecosystem_analysis() -> None:
    output = analyze(Website("site-1", "https://example.org", "example.org", description="DeFi ecosystem protocol"))
    assert "Strong Ecosystem Presence" in finding_types(output)
    assert "Ecosystem Presence" in assessment_types(output)


def test_communication_analysis() -> None:
    output = analyze(Link("link-1", "page-1", "https://x.com/project", "Twitter"))
    assert "Strong Communication" in finding_types(output)
    assert "Communication Quality" in assessment_types(output)


def test_runtime_delegation_excludes_signals() -> None:
    output = analyze(Website("site-1", "https://example.org", "example.org", description="DeFi ecosystem"))
    received = []

    def runtime_entrypoint(canonical_output, context):
        received.append(canonical_output)
        return ExecutionResult(context.execution_id, ExecutionState.COMPLETED)

    context = ExecutionContext("execution-1", "1.0", NOW)
    result = WebsiteAnalysisEngine.enter_runtime(
        output, WebsiteRuntimeIntegration(RuntimeFacade(runtime_entrypoint)), context
    )
    assert result.final_state is ExecutionState.COMPLETED
    assert received[0][0:4] == (
        output.observation, output.evidence, output.findings, output.assessments
    )
    assert received[0][4] == ()
