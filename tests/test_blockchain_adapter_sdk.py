from src.blockchain_platform.adapters import AdapterContext, AdapterRegistry, AdapterResult, BlockchainAdapter, BlockchainProvider, DuplicateAdapterError, DuplicateProviderError, EVMAdapter, EthereumAdapter, ProviderMetadata, ProviderRegistry, SolanaAdapter
from src.core_intelligence.onchain import Address, ChainReference, Token, Wallet


class ProviderFixture:
    def metadata(self):
        return ProviderMetadata("provider-1", "Provider", "1.0", ("network-1",), ("wallets",))

    def discover_wallet(self, identifier): return {"id": identifier}
    def discover_transactions(self, identifier): return ()
    def discover_contracts(self, identifier): return ()
    def discover_tokens(self, identifier): return ()
    def discover_nfts(self, identifier): return ()
    def discover_protocols(self, identifier): return ()
    def discover_governance(self, identifier): return ()


class AdapterFixture:
    adapter_id = "adapter-1"


def test_provider_and_adapter_protocols() -> None:
    assert "discover_wallet" in BlockchainProvider.__dict__
    assert "adapt" in BlockchainAdapter.__dict__
    assert EVMAdapter.__mro__[1] is BlockchainAdapter
    assert EthereumAdapter.__mro__[1] is EVMAdapter
    assert SolanaAdapter.__mro__[1] is BlockchainAdapter


def test_provider_metadata_and_context_are_immutable() -> None:
    metadata = ProviderFixture().metadata()
    context = AdapterContext(metadata.provider_id, ChainReference("network-1"), "2026-08-08T00:00:00Z")
    assert metadata.supported_chains == ("network-1",)
    assert context.chain.chain_id == "network-1"


def test_provider_registry() -> None:
    provider = ProviderFixture()
    registry = ProviderRegistry()
    registry.register(provider)
    assert registry.get("provider-1") is provider
    try:
        registry.register(provider)
    except DuplicateProviderError:
        return
    raise AssertionError("duplicate provider was accepted")


def test_adapter_registry() -> None:
    adapter = AdapterFixture()
    registry = AdapterRegistry()
    registry.register(adapter)
    assert registry.get("adapter-1") is adapter
    try:
        registry.register(adapter)
    except DuplicateAdapterError:
        return
    raise AssertionError("duplicate adapter was accepted")


def test_adapter_result_contains_canonical_models() -> None:
    wallet = Wallet("wallet-1", (Address("address-1", ChainReference("network-1")),))
    result = AdapterResult(wallets=(wallet,), tokens=(Token("token-1", "TKN"),))
    assert result.wallets[0] is wallet
    assert result.tokens[0].symbol == "TKN"
