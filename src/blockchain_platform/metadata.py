from src.platform_sdk import IntegrationMetadata


BLOCKCHAIN_PLATFORM_METADATA = IntegrationMetadata(
    collector="BlockchainCollector",
    source="blockchain",
    adapter="BlockchainAdapter",
    version="0.5.0",
    capabilities=("chains", "capabilities", "endpoints", "metadata"),
    supported_entity_types=("blockchain",),
    supported_observation_types=("blockchain", "chain_capability", "chain_endpoint", "chain_metadata"),
)
