from datetime import UTC, datetime

from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.twitter_intelligence import (
    TwitterDiscoveryEngine,
    TwitterPost,
    TwitterProfile,
    TwitterRuntimeIntegration,
)
from src.twitter_intelligence.discovery.discovery_result import DiscoveredEntityType
from src.twitter_intelligence.discovery.hashtag_discovery import HashtagDiscovery
from src.twitter_intelligence.discovery.mention_discovery import MentionDiscovery
from src.twitter_intelligence.discovery.reply_discovery import ReplyDiscovery
from src.twitter_intelligence.discovery.url_discovery import URLDiscovery


NOW = datetime(2026, 8, 7, tzinfo=UTC)


def make_post(text: str, post_id: str = "post-1", conversation_id: str | None = None) -> TwitterPost:
    return TwitterPost(post_id, "user-1", text, NOW, conversation_id)


def values(entities, entity_type: DiscoveredEntityType) -> set[str]:
    return {entity.normalized_value for entity in entities if entity.entity_type is entity_type}


def test_profile_discovery() -> None:
    result = TwitterDiscoveryEngine().discover_profile(
        TwitterProfile("user-1", "CryptoIntel", "Crypto Intel", "Visit https://example.com")
    )
    assert result.discovery_type == "profile"
    assert result.observation.source_identifier == "user-1"
    assert values(result.entities, DiscoveredEntityType.USERNAME) == {"cryptointel"}


def test_post_discovery() -> None:
    result = TwitterDiscoveryEngine().discover_post(make_post("Crypto update"))
    assert result.discovery_type == "post"
    assert result.observation.raw_payload["text"] == "Crypto update"


def test_thread_discovery() -> None:
    posts = (make_post("First", "post-1", "thread-1"), make_post("Second", "post-2", "thread-1"))
    result = TwitterDiscoveryEngine().discover_thread(posts)
    assert result.discovery_type == "thread"
    assert result.observation.source_identifier == "thread-1"
    assert len(result.children) == 2


def test_reply_discovery() -> None:
    result = ReplyDiscovery().discover(make_post("Reply"))
    assert result.discovery_type == "reply"
    assert result.observation.source_identifier == "post-1"


def test_mention_extraction() -> None:
    entities = MentionDiscovery().discover(make_post("Hello @CryptoIntel"))
    assert values(entities, DiscoveredEntityType.MENTION) == {"cryptointel"}


def test_hashtag_and_cashtag_extraction() -> None:
    entities = HashtagDiscovery().discover(make_post("Tracking #DeFi and $ETH"))
    assert values(entities, DiscoveredEntityType.HASHTAG) == {"defi"}
    assert values(entities, DiscoveredEntityType.CASHTAG) == {"ETH"}


def test_url_and_website_extraction() -> None:
    entities = URLDiscovery().discover(make_post("Visit https://Example.com/docs"))
    assert values(entities, DiscoveredEntityType.URL) == {"https://example.com/docs"}
    assert values(entities, DiscoveredEntityType.WEBSITE) == {"https://example.com/docs"}


def test_github_url_extraction() -> None:
    entities = URLDiscovery().discover(make_post("https://github.com/OpenAI/Codex"))
    assert values(entities, DiscoveredEntityType.GITHUB_ORGANIZATION) == {"openai"}
    assert values(entities, DiscoveredEntityType.GITHUB_REPOSITORY) == {"openai/codex"}


def test_discord_invite_extraction() -> None:
    entities = URLDiscovery().discover(make_post("https://discord.gg/CryptoIntel"))
    assert values(entities, DiscoveredEntityType.DISCORD_INVITE) == {"https://discord.gg/CryptoIntel"}


def test_telegram_link_extraction() -> None:
    entities = URLDiscovery().discover(make_post("https://t.me/CryptoIntel"))
    assert values(entities, DiscoveredEntityType.TELEGRAM_LINK) == {"https://t.me/CryptoIntel"}


def test_gitbook_and_documentation_extraction() -> None:
    entities = URLDiscovery().discover(make_post("https://project.gitbook.io/docs"))
    assert values(entities, DiscoveredEntityType.GITBOOK_LINK) == {"https://project.gitbook.io/docs"}
    assert values(entities, DiscoveredEntityType.DOCUMENTATION_LINK) == {"https://project.gitbook.io/docs"}


def test_email_extraction() -> None:
    result = TwitterDiscoveryEngine().discover_post(make_post("Contact Team@Example.com"))
    assert values(result.entities, DiscoveredEntityType.EMAIL) == {"team@example.com"}


def test_runtime_delegation_preserves_all_discovery_results() -> None:
    engine = TwitterDiscoveryEngine()
    results = (engine.discover_post(make_post("First", "post-1")), engine.discover_post(make_post("Second", "post-2")))
    received = []

    def runtime_entrypoint(output, context):
        received.append((output, context))
        return ExecutionResult(context.execution_id, ExecutionState.COMPLETED)

    context = ExecutionContext("execution-1", "1.0", NOW)
    outcome = engine.enter_runtime(
        results, TwitterRuntimeIntegration(RuntimeFacade(runtime_entrypoint)), context
    )

    assert outcome.final_state is ExecutionState.COMPLETED
    observation = received[0][0][0]
    assert observation.observation_id.startswith("twitter:discovery:batch:")
    assert [item["discovery_id"] for item in observation.raw_payload["results"]] == [
        "twitter:post:post-1", "twitter:post:post-2"
    ]
