from src.platform_sdk import IntegrationMetadata


WALLET_INTELLIGENCE_METADATA = IntegrationMetadata(
    collector="BlockchainAdapterSDK",
    source="wallet",
    adapter="WalletDiscovery,WalletClassificationEngine",
    version="0.5.0",
    capabilities=("wallet_discovery", "wallet_classification", "labels", "profiles"),
    supported_entity_types=("wallet", "address", "chain_account"),
    supported_observation_types=("wallet_profile", "wallet_classification"),
)
