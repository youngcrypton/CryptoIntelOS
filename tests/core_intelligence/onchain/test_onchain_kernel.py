from dataclasses import FrozenInstanceError

from src.core_intelligence.onchain import (
    Address, BlockReference, ChainAccount, ChainReference, Contract, NFT, NFTCollection,
    OnChainContext, OnChainRegistry, OnChainType, Token, Transaction, TransactionFee,
    Transfer, Wallet,
)


def test_identity_and_transaction_models_serialize() -> None:
    chain = ChainReference("network-1", "mainnet", "namespace")
    address = Address("address-1", chain, "primary")
    wallet = Wallet("wallet-1", (address,), "Treasury")
    transaction = Transaction(
        "tx-1", chain, BlockReference("block-1", 42, "2026-08-08T00:00:00Z"),
        "confirmed", (Transfer("transfer-1", "a", "b", "ASSET", "10"),),
        TransactionFee("1", "ASSET"),
    )
    serialized = transaction.to_dict()
    assert serialized["chain"]["chain_id"] == "network-1"
    assert serialized["transfers"][0]["amount"] == "10"
    assert wallet.to_dict()["addresses"][0]["value"] == "address-1"


def test_models_are_immutable() -> None:
    token = Token("token-1", "TKN", "Token", 18)
    try:
        token.symbol = "CHANGED"
    except FrozenInstanceError:
        return
    raise AssertionError("canonical model was mutable")


def test_asset_contract_models_and_references() -> None:
    chain = ChainReference("network-1")
    contract = Contract("contract-1", "contract-address", chain, "Vault")
    nft = NFT("nft-1", NFTCollection("collection-1", "Collection"), "7", "owner")
    account = ChainAccount("account-1", Address("address-1", chain), chain)
    assert contract.chain is chain
    assert nft.collection.collection_id == "collection-1"
    assert account.address.chain is chain


def test_enum_integrity() -> None:
    assert {item.value for item in OnChainType} >= {"wallet", "transaction", "token", "contract"}


def test_context_and_registry_are_contracts() -> None:
    context = OnChainContext("source-a", ChainReference("network-1"), "2026-08-08T00:00:00Z", "corr-1")
    assert context.chain.chain_id == "network-1"
    assert "register" in OnChainRegistry.__dict__
    assert "get" in OnChainRegistry.__dict__
    assert "supports" in OnChainRegistry.__dict__
