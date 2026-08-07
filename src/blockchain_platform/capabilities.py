from enum import StrEnum


class BlockchainCapability(StrEnum):
    """Descriptive capabilities exposed by a blockchain network."""

    SMART_CONTRACTS = "smart_contracts"
    TOKENS = "tokens"
    NFTS = "nfts"
    GOVERNANCE = "governance"
    VALIDATORS = "validators"
    STAKING = "staking"
    DEX = "dex"
    BRIDGES = "bridges"
    NAME_SERVICE = "name_service"
