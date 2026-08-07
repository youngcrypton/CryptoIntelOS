from datetime import UTC, datetime

from src.core_intelligence.models import Observation
from src.platform_sdk import SourceAdapter, SourceCollector
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.twitter_intelligence import (
    TWITTER_INTEGRATION_METADATA,
    TwitterCollector,
    TwitterPost,
    TwitterPostAdapter,
    TwitterProfile,
    TwitterProfileAdapter,
    TwitterRuntimeIntegration,
)


def test_collector_and_adapter_contracts_use_platform_sdk() -> None:
    assert "collect" in SourceCollector.__dict__
    assert "to_observation" in SourceAdapter.__dict__
    assert TwitterCollector.__mro__[1] is SourceCollector
    assert TwitterPostAdapter.__mro__[1] is SourceAdapter
    assert TwitterProfileAdapter.__mro__[1] is SourceAdapter


def test_models_and_metadata_are_source_specific() -> None:
    post = TwitterPost("post-1", "user-1", "Crypto update", datetime.now(UTC))
    profile = TwitterProfile("user-1", "cryptointel")
    assert post.author_id == profile.user_id
    assert TWITTER_INTEGRATION_METADATA.source == "twitter"
    assert TWITTER_INTEGRATION_METADATA.version == "0.3.0"
    assert TWITTER_INTEGRATION_METADATA.supported_observation_types == (
        "twitter_post",
        "twitter_profile",
    )


def test_runtime_integration_delegates_through_sdk_facade() -> None:
    observed_at = datetime.now(UTC)
    observation = Observation(
        "twitter:post:1",
        "twitter",
        "post-1",
        "twitter-api",
        observed_at,
        observed_at,
        "0.3.0",
        "checksum",
        {"text": "Crypto update"},
    )
    context = ExecutionContext("execution-1", "1.0", observed_at)
    calls = []

    def runtime_entrypoint(output, supplied_context):
        calls.append((output, supplied_context))
        return ExecutionResult(supplied_context.execution_id, ExecutionState.COMPLETED)

    from src.platform_sdk import RuntimeFacade

    result = TwitterRuntimeIntegration(RuntimeFacade(runtime_entrypoint)).integrate(
        (observation, (), (), (), ()), context
    )
    assert result.final_state is ExecutionState.COMPLETED
    assert calls[0][0][0].source == "twitter"
