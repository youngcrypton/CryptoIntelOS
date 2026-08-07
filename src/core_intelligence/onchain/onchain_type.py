from enum import StrEnum


class OnChainType(StrEnum):
    WALLET = "wallet"
    ADDRESS = "address"
    TRANSACTION = "transaction"
    TOKEN = "token"
    NFT = "nft"
    CONTRACT = "contract"
    GOVERNANCE = "governance"
    VALIDATOR = "validator"
