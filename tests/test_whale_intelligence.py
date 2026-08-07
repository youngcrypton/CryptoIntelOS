from io import StringIO

from src.blockchain_platform.adapters import AdapterContext, AdapterResult, ProviderMetadata
from src.core_intelligence.onchain import Address, ChainReference, Wallet
from src.runtime.correlation import CorrelationStatus
from src.runtime.engine import ExecutionState
from src.wallet_intelligence.intelligence import DeterministicScoringStrategy, ScoringStrategy, WalletIntelligenceVerticalSlice, WhaleCategory, WhaleIntelligenceEngine, WhaleRegistry


class Provider:
    def metadata(self): return ProviderMetadata("provider-1", "Provider", "1.0")


class Adapter:
    adapter_id = "adapter-1"
    def adapt(self, provider, identifier, context):
        return AdapterResult(wallets=(Wallet(identifier, (Address("address-1", context.chain),), "Smart Money Treasury"),))


METRICS = (("capital", 90.0), ("behavior", 85.0), ("influence", 70.0), ("network", 65.0), ("historical", 88.0), ("cross_chain", 75.0), ("confidence", 95.0))


def result():
    from src.wallet_intelligence import WalletClassificationEngine, WalletDiscovery
    discovered = WalletDiscovery().discover(Adapter().adapt(Provider(), "wallet-1", AdapterContext("provider-1", ChainReference("network-1"))))
    classified = WalletClassificationEngine().classify(discovered)[0]
    return WhaleIntelligenceEngine().analyze(classified, METRICS)


def test_whale_profile_and_independent_scores() -> None:
    output = result()
    assert output.profile.canonical_identifier == "whale:wallet-1"
    assert output.profile.scores.capital.value == 90
    assert output.profile.scores.behavior.value == 85
    assert WhaleCategory.SMART_MONEY in output.profile.categories
    assert WhaleCategory.HIGH_CONVICTION in output.profile.categories
    assert output.profile.supporting_evidence


def test_registry_and_strategy_contract() -> None:
    profile = result().profile
    registry = WhaleRegistry()
    registry.register(profile)
    assert registry.get(profile.canonical_identifier) is profile
    assert "score" in ScoringStrategy.__dict__
    assert isinstance(DeterministicScoringStrategy().score((), METRICS).capital.value, float)


def test_complete_wallet_intelligence_execution_path() -> None:
    console = StringIO()
    execution = WalletIntelligenceVerticalSlice().run(Provider(), Adapter(), "wallet-1", AdapterContext("provider-1", ChainReference("network-1")), METRICS, output=console)
    assert execution.runtime.compilation.projection.nodes
    assert len(execution.runtime.graph.nodes) == len(execution.runtime.compilation.projection.nodes)
    assert execution.runtime.correlation.status is CorrelationStatus.CONFIRMED
    assert execution.runtime.automation.actions
    assert execution.runtime.distribution.requests
    assert execution.runtime.execution.final_state is ExecutionState.COMPLETED
    for phrase in ("Provider", "Adapter", "Canonical Wallet", "Wallet Discovery", "Wallet Classification", "Whale Intelligence", "Compiler Executed", "Knowledge Graph Updated", "Correlation Completed", "Reasoning Completed", "Automation Plan Created", "Distribution Plan Created", "Execution Successful"):
        assert phrase in console.getvalue()
