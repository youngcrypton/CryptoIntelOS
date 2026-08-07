from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

from src.blockchain_platform import BLOCKCHAIN_PLATFORM_METADATA, Blockchain, BlockchainAdapter, BlockchainCapability, BlockchainCollector, BlockchainRegistry, BlockchainRuntimeIntegration, BlockchainValidator, ChainCapability, ChainEndpoint, ChainMetadata, DuplicateBlockchainError, TransportType, ValidationResult
from src.core_intelligence.models import Observation
from src.platform_sdk import RuntimeFacade, SourceAdapter, SourceCollector
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState


def blockchain() -> Blockchain:
    capabilities = (ChainCapability(BlockchainCapability.SMART_CONTRACTS), ChainCapability(BlockchainCapability.STAKING))
    metadata = ChainMetadata("eip155:1", "mainnet", "ETH", capabilities, "https://etherscan.io")
    endpoint = ChainEndpoint("ethereum-rpc", metadata.chain_id, "https://rpc.example", TransportType.RPC)
    return Blockchain(metadata.chain_id, "Ethereum", "ethereum", metadata, (endpoint,))


def test_protocols_use_platform_sdk() -> None:
    assert BlockchainCollector.__mro__[1] is SourceCollector
    assert BlockchainAdapter.__mro__[1] is SourceAdapter
    assert "validate" in BlockchainValidator.__mro__[1].__dict__


def test_models_are_immutable_and_descriptive() -> None:
    chain = blockchain()
    assert chain.metadata.capabilities[0].capability is BlockchainCapability.SMART_CONTRACTS
    assert chain.endpoints[0].transport is TransportType.RPC
    try:
        chain.name = "Changed"
    except FrozenInstanceError:
        return
    raise AssertionError("Blockchain model was mutable")


def test_metadata_describes_platform_foundation() -> None:
    assert BLOCKCHAIN_PLATFORM_METADATA.source == "blockchain"
    assert BLOCKCHAIN_PLATFORM_METADATA.version == "0.5.0"
    assert "endpoints" in BLOCKCHAIN_PLATFORM_METADATA.capabilities


def test_registry_is_ordered_and_rejects_duplicates() -> None:
    chain = blockchain()
    registry = BlockchainRegistry()
    registry.register(chain)
    assert registry.get(chain.chain_id) is chain
    assert registry.all() == (chain,)
    try:
        registry.register(chain)
    except DuplicateBlockchainError:
        return
    raise AssertionError("duplicate blockchain was accepted")


def test_runtime_integration_delegates_canonical_output() -> None:
    timestamp = datetime(2026, 8, 7, tzinfo=UTC)
    observation = Observation("blockchain:eip155:1", "blockchain", "eip155:1", "blockchain-platform", timestamp, timestamp, "0.5.0", "checksum", {"name": "Ethereum"})
    context = ExecutionContext("execution-1", "1.0", timestamp)
    calls = []

    def entrypoint(output, supplied_context):
        calls.append((output, supplied_context))
        return ExecutionResult(supplied_context.execution_id, ExecutionState.COMPLETED)

    result = BlockchainRuntimeIntegration(RuntimeFacade(entrypoint)).integrate((observation, (), (), (), ()), context)
    assert result.final_state is ExecutionState.COMPLETED
    assert calls == [((observation, (), (), (), ()), context)]


def test_validation_result_is_immutable() -> None:
    result = ValidationResult(False, ("chain_id is required",))
    assert not result.valid
    assert result.errors == ("chain_id is required",)
