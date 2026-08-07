from datetime import UTC, datetime

from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.website_intelligence import Document, Link, Page, Website, WebsiteRuntimeIntegration
from src.website_intelligence.discovery import (
    ContactDiscovery,
    DiscoveredEntityType,
    NavigationDiscovery,
    SocialDiscovery,
    WebsiteDiscoveryEngine,
    WebsiteEntityExtractor,
)


NOW = datetime(2026, 8, 7, tzinfo=UTC)


def values(entities, entity_type: DiscoveredEntityType) -> set[str]:
    return {item.normalized_value for item in entities if item.entity_type is entity_type}


def test_website_discovery() -> None:
    result = WebsiteDiscoveryEngine().discover_website(
        Website("site-1", "https://Example.org", "example.org", "Example")
    )
    assert result.discovery_type == "website"
    assert result.observation.source == "website"
    assert values(result.entities, DiscoveredEntityType.DOMAIN) == {"example.org"}


def test_page_discovery() -> None:
    result = WebsiteDiscoveryEngine().discover_page(
        Page("page-1", "site-1", "https://example.org/roadmap", "Roadmap")
    )
    assert result.discovery_type == "page"
    assert values(result.entities, DiscoveredEntityType.ROADMAP)


def test_document_discovery() -> None:
    result = WebsiteDiscoveryEngine().discover_document(
        Document("doc-1", "site-1", "https://example.org/paper.pdf", "whitepaper")
    )
    assert values(result.entities, DiscoveredEntityType.WHITEPAPER)


def test_navigation_discovery() -> None:
    entities = NavigationDiscovery().discover((("Docs", "/docs"), ("Careers", "/careers")))
    assert values(entities, DiscoveredEntityType.NAVIGATION) == {"/docs", "/careers"}


def test_social_link_extraction() -> None:
    entities = SocialDiscovery().discover(("https://linkedin.com/company/project", "https://youtube.com/@project", "https://medium.com/project"))
    assert values(entities, DiscoveredEntityType.LINKEDIN_LINK)
    assert values(entities, DiscoveredEntityType.YOUTUBE_LINK)
    assert values(entities, DiscoveredEntityType.MEDIUM_LINK)


def test_github_extraction() -> None:
    entities = WebsiteEntityExtractor().extract(urls=("https://github.com/OpenAI/Codex",))
    assert values(entities, DiscoveredEntityType.GITHUB_REPOSITORY) == {"openai/codex"}


def test_twitter_extraction() -> None:
    entities = WebsiteEntityExtractor().extract(urls=("https://x.com/CryptoProject",))
    assert values(entities, DiscoveredEntityType.TWITTER_ACCOUNT) == {"cryptoproject"}


def test_discord_extraction() -> None:
    entities = WebsiteEntityExtractor().extract(urls=("https://discord.gg/project",))
    assert values(entities, DiscoveredEntityType.DISCORD_INVITE)


def test_telegram_extraction() -> None:
    entities = WebsiteEntityExtractor().extract(urls=("https://t.me/project",))
    assert values(entities, DiscoveredEntityType.TELEGRAM_LINK)


def test_gitbook_extraction() -> None:
    entities = WebsiteEntityExtractor().extract(urls=("https://project.gitbook.io/docs",))
    assert values(entities, DiscoveredEntityType.GITBOOK)
    assert values(entities, DiscoveredEntityType.DOCUMENTATION)


def test_whitepaper_extraction() -> None:
    entities = WebsiteEntityExtractor().extract(urls=("https://example.org/whitepaper",))
    assert values(entities, DiscoveredEntityType.WHITEPAPER)


def test_email_extraction() -> None:
    entities = ContactDiscovery().discover("Contact Team@Example.org")
    assert values(entities, DiscoveredEntityType.EMAIL) == {"team@example.org"}


def test_runtime_delegation_preserves_all_observations() -> None:
    engine = WebsiteDiscoveryEngine()
    results = (
        engine.discover_website(Website("site-1", "https://example.org", "example.org")),
        engine.discover_page(Page("page-1", "site-1", "https://example.org/docs")),
    )
    received = []

    def runtime_entrypoint(output, context):
        received.append(output)
        return ExecutionResult(context.execution_id, ExecutionState.COMPLETED)

    context = ExecutionContext("execution-1", "1.0", NOW)
    result = engine.enter_runtime(
        results, WebsiteRuntimeIntegration(RuntimeFacade(runtime_entrypoint)), context
    )
    assert result.final_state is ExecutionState.COMPLETED
    observation = received[0][0]
    assert observation.observation_id.startswith("website:discovery:batch:")
    assert len(observation.raw_payload["results"]) == 2
