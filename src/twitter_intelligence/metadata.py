from src.platform_sdk import IntegrationMetadata


TWITTER_INTEGRATION_METADATA = IntegrationMetadata(
    collector="TwitterCollector",
    source="twitter",
    adapter="TwitterPostAdapter,TwitterProfileAdapter",
    version="0.3.0",
    capabilities=("posts", "profiles"),
    supported_entity_types=("person", "organization", "project"),
    supported_observation_types=("twitter_post", "twitter_profile"),
)
