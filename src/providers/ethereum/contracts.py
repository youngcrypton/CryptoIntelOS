from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from src.core_intelligence.models import Observation
from src.providers.connectors import ConnectorContext, ConnectorMetadata, ConnectorPolicy, ConnectorResult
from src.providers.providers import ProviderContext, ProviderMetadata, ProviderPolicy, ProviderResult
from src.providers.adapters import AdapterContext, AdapterMetadata, AdapterResult
class EthereumProviderError(Exception): pass
class JsonRpcError(EthereumProviderError): pass
@dataclass(frozen=True, slots=True)
class EthereumConfig: endpoint: str; chain_id: str = "1"; api_key: str | None = None; timeout_seconds: float = 30.0
@dataclass(frozen=True, slots=True)
class EthereumRpcConnector:
    config: EthereumConfig; transport: Any = None; metadata: ConnectorMetadata = field(default_factory=lambda: ConnectorMetadata("ethereum-rpc", "Ethereum JSON-RPC"))
    def request(self, operation: str, context: ConnectorContext, policy: ConnectorPolicy) -> ConnectorResult:
        if self.transport is None: raise EthereumProviderError("RPC transport is not configured")
        return ConnectorResult(self.metadata.connector_id, True, self.transport.call(operation, timeout=policy.timeout_seconds))
@dataclass(frozen=True, slots=True)
class EthereumProvider:
    connector: EthereumRpcConnector; metadata: ProviderMetadata = field(default_factory=lambda: ProviderMetadata("ethereum", "Ethereum", source="ethereum"))
    def query(self, method: str, params: tuple[Any, ...], context: ProviderContext) -> ProviderResult:
        result = self.connector.request(method, ConnectorContext(context.correlation_id, context.execution_id), ConnectorPolicy(self.connector.config.timeout_seconds)); return ProviderResult(self.metadata.provider_id, result.success, result.payload, result.error, (("chain_id", self.connector.config.chain_id),))
class EthereumBlockProvider(EthereumProvider): pass
class EthereumTransactionProvider(EthereumProvider): pass
class EthereumWalletProvider(EthereumProvider): pass
class EthereumTokenProvider(EthereumProvider): pass
class EthereumContractProvider(EthereumProvider): pass
class EthereumNftProvider(EthereumProvider): pass
class EthereumLogProvider(EthereumProvider): pass
class EthereumBalanceProvider(EthereumProvider): pass
@dataclass(frozen=True, slots=True)
class EthereumAdapter:
    metadata: AdapterMetadata = field(default_factory=lambda: AdapterMetadata("ethereum-canonical", "Ethereum Canonical Adapter"))
    def adapt(self, result: ProviderResult, context: AdapterContext) -> AdapterResult:
        payload = result.value if isinstance(result.value, dict) else {"value": result.value}; ident = str(payload.get("hash", payload.get("number", context.execution_id)))
        return AdapterResult(self.metadata.adapter_id, (Observation(f"ethereum:{ident}", "ethereum", ident, "json-rpc", __import__("datetime").datetime.now(__import__("datetime").UTC), __import__("datetime").datetime.now(__import__("datetime").UTC), "ethereum-adapter-1", ident, payload),), result.provenance)
