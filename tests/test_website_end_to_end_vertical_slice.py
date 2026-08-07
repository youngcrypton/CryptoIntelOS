from datetime import UTC, datetime
from io import StringIO

from src.runtime.correlation import CorrelationStatus
from src.runtime.distribution import DistributionStatus
from src.runtime.engine import ExecutionState
from src.runtime.reasoning import ReasoningStatus
from src.website_intelligence import Document, Link, Page, Website, WebsiteVerticalSlice


def test_website_end_to_end_vertical_slice() -> None:
    timestamp = datetime(2026, 8, 7, tzinfo=UTC)
    website = Website(
        "site-1",
        "https://example.org",
        "example.org",
        "Example Protocol",
        "Official DeFi ecosystem protocol",
    )
    pages = (
        Page("page-team", website.website_id, "https://example.org/team", "Team"),
        Page("page-roadmap", website.website_id, "https://example.org/roadmap", "Roadmap"),
        Page("page-careers", website.website_id, "https://example.org/careers", "We're hiring"),
        Page("page-audits", website.website_id, "https://example.org/audits", "Security Audits"),
    )
    documents = (
        Document("doc-1", website.website_id, "https://example.org/docs", "documentation", "Documentation", timestamp, timestamp),
    )
    links = (
        Link("link-1", "page-team", "https://x.com/example", "Twitter"),
    )
    console = StringIO()

    result = WebsiteVerticalSlice().run(
        website, pages=pages, documents=documents, links=links, output=console
    )

    assert len(result.discoveries) == 1 + len(pages) + len(documents) + len(links)
    assert result.canonical.observation.source == "website"
    assert result.canonical.evidence
    assert result.canonical.findings
    assert result.canonical.assessments
    assert result.canonical.signals
    expected_nodes = 1 + len(result.canonical.evidence) + len(result.canonical.findings) + len(result.canonical.assessments) + len(result.canonical.signals)
    assert len(result.runtime.compilation.projection.nodes) == expected_nodes
    assert len(result.runtime.graph.nodes) == expected_nodes
    assert result.runtime.correlation.status is CorrelationStatus.CONFIRMED
    assert result.runtime.reasoning.status is ReasoningStatus.COMPLETED
    assert result.runtime.automation.actions
    assert result.runtime.distribution.requests
    assert result.runtime.distribution_results[0].status is DistributionStatus.ACCEPTED
    assert result.runtime.execution.final_state is ExecutionState.COMPLETED
    for phrase in ("Website Processed", "Pages Discovered", "Documents Discovered", "Observations Created", "Evidence Generated", "Findings Generated", "Assessments Produced", "Signals Generated", "Compiler Executed", "Knowledge Graph Updated", "Correlation Completed", "Reasoning Completed", "Automation Plan Created", "Distribution Plan Created", "Execution Successful"):
        assert phrase in console.getvalue()
