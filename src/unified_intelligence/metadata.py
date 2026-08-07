from src.platform_sdk import IntegrationMetadata


UNIFIED_INTELLIGENCE_METADATA = IntegrationMetadata(
    collector="EntityLinker",
    source="unified_intelligence",
    adapter="DeterministicEntityResolution",
    version="0.6.0",
    capabilities=("entity_linking", "identity_bundles", "traceability"),
    supported_entity_types=("project", "organization", "repository", "account", "wallet", "domain"),
    supported_observation_types=("identity_bundle",),
)
