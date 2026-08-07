from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

from src.core_intelligence.models import Observation
from src.platform_sdk import RuntimeFacade, SourceAdapter, SourceCollector
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.website_intelligence import (
    WEBSITE_INTEGRATION_METADATA,
    Document,
    DocumentAdapter,
    Link,
    LinkAdapter,
    Page,
    PageAdapter,
    Website,
    WebsiteAdapter,
    WebsiteCollector,
    WebsiteRuntimeIntegration,
)


def test_collector_contract_uses_platform_sdk() -> None:
    assert "collect" in SourceCollector.__dict__
    assert WebsiteCollector.__mro__[1] is SourceCollector


def test_adapter_contracts_use_platform_sdk() -> None:
    assert "to_observation" in SourceAdapter.__dict__
    assert WebsiteAdapter.__mro__[1] is SourceAdapter
    assert PageAdapter.__mro__[1] is SourceAdapter
    assert LinkAdapter.__mro__[1] is SourceAdapter
    assert DocumentAdapter.__mro__[1] is SourceAdapter


def test_metadata_describes_website_integration() -> None:
    assert WEBSITE_INTEGRATION_METADATA.source == "website"
    assert WEBSITE_INTEGRATION_METADATA.version == "0.4.0"
    assert WEBSITE_INTEGRATION_METADATA.capabilities == (
        "websites",
        "pages",
        "links",
        "documents",
    )
    assert WEBSITE_INTEGRATION_METADATA.supported_observation_types == (
        "website",
        "website_page",
        "website_link",
        "website_document",
    )


def test_source_models_are_immutable_and_related_by_identifiers() -> None:
    timestamp = datetime(2026, 8, 7, tzinfo=UTC)
    website = Website("site-1", "https://example.org", "example.org", "Example")
    page = Page("page-1", website.website_id, "https://example.org/about")
    link = Link("link-1", page.page_id, "https://docs.example.org", "Docs")
    document = Document(
        "doc-1",
        website.website_id,
        "https://example.org/whitepaper.pdf",
        "whitepaper",
        published_at=timestamp,
    )
    assert page.website_id == document.website_id == website.website_id
    assert link.source_page_id == page.page_id
    try:
        website.domain = "changed.example"
    except FrozenInstanceError:
        return
    raise AssertionError("Website model was mutable")


def test_runtime_integration_delegates_canonical_output() -> None:
    observed_at = datetime(2026, 8, 7, tzinfo=UTC)
    observation = Observation(
        "website:site-1",
        "website",
        "site-1",
        "website-source",
        observed_at,
        observed_at,
        "0.4.0",
        "checksum",
        {"url": "https://example.org"},
    )
    context = ExecutionContext("execution-1", "1.0", observed_at)
    calls = []

    def runtime_entrypoint(output, supplied_context):
        calls.append((output, supplied_context))
        return ExecutionResult(supplied_context.execution_id, ExecutionState.COMPLETED)

    result = WebsiteRuntimeIntegration(RuntimeFacade(runtime_entrypoint)).integrate(
        (observation, (), (), (), ()), context
    )
    assert result.final_state is ExecutionState.COMPLETED
    assert calls == [((observation, (), (), (), ()), context)]
