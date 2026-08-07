from datetime import UTC, datetime

from src.blockchain_platform.adapters import AdapterResult
from src.core_intelligence.onchain import Address, ChainReference, Wallet
from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionState, ExecutionResult
from src.wallet_intelligence import LabelType, WalletClassificationEngine, WalletDiscovery, WalletRuntimeIntegration


def test_discovery_profiles_wallet_kinds_and_names() -> None:
    wallet = Wallet("wallet-1", (Address("address-1", ChainReference("network-1")),), "Project Treasury")
    result = WalletDiscovery().discover(AdapterResult(wallets=(wallet,)), {"wallet-1": {"wallet_type": "multisig", "ens_name": "treasury.eth"}})
    profile = result.profiles[0]
    assert profile.wallet_type == "multisig"
    assert profile.ens_name == "treasury.eth"
    assert profile.wallet.wallet_id == "wallet-1"


def test_classification_is_deterministic_and_supports_unknown() -> None:
    wallets = (Wallet("treasury", label="Foundation treasury"), Wallet("unknown"))
    discovered = WalletDiscovery().discover(AdapterResult(wallets=wallets))
    classified = WalletClassificationEngine().classify(discovered)
    assert LabelType.FOUNDATION in {label.label_type for label in classified[0].labels}
    assert classified[1].labels[0].label_type is LabelType.UNKNOWN


def test_labels_and_profiles_are_immutable() -> None:
    wallet = Wallet("wallet-1")
    profile = WalletDiscovery().discover(AdapterResult(wallets=(wallet,))).profiles[0]
    labels = WalletClassificationEngine().classify(type("Result", (), {"profiles": (profile,)})())[0].labels
    assert labels[0].value == "unknown"
    try:
        profile.wallet_type = "changed"
    except AttributeError:
        return
    raise AssertionError("WalletProfile was mutable")


def test_runtime_delegation_forwards_canonical_output() -> None:
    timestamp = datetime(2026, 8, 8, tzinfo=UTC)
    context = ExecutionContext("execution-1", "1.0", timestamp)
    received = []

    def entrypoint(output, supplied_context):
        received.append((output, supplied_context))
        return ExecutionResult(supplied_context.execution_id, ExecutionState.COMPLETED)

    output = ("wallet-profile", (), (), (), ())
    result = WalletRuntimeIntegration(RuntimeFacade(entrypoint)).integrate(output, context)
    assert result.final_state is ExecutionState.COMPLETED
    assert received == [(output, context)]
