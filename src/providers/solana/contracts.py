from src.providers.ethereum.contracts import EthereumConfig, EthereumRpcConnector
SolanaConfig = EthereumConfig
class SolanaRpcConnector(EthereumRpcConnector): pass
class SolanaProvider:
    def __init__(self, connector): self.connector = connector
    def query(self, method, params, context):
        from src.providers.providers import ProviderResult
        from src.providers.connectors import ConnectorContext, ConnectorPolicy
        result = self.connector.request(method, ConnectorContext(context.correlation_id, context.execution_id), ConnectorPolicy(self.connector.config.timeout_seconds))
        return ProviderResult("solana", result.success, result.payload, result.error, (("network", self.connector.config.chain_id),))
class SolanaAccountProvider(SolanaProvider): pass
class SolanaProgramProvider(SolanaProvider): pass
class SolanaTokenProvider(SolanaProvider): pass
class SolanaNftProvider(SolanaProvider): pass
class SolanaTransactionProvider(SolanaProvider): pass
class SolanaBlockProvider(SolanaProvider): pass
class SolanaSlotProvider(SolanaProvider): pass
class SolanaMetadataProvider(SolanaProvider): pass
class SolanaAdapter:
    metadata = __import__('src.providers.adapters', fromlist=['AdapterMetadata']).AdapterMetadata('solana-canonical', 'Solana Canonical Adapter')
    def adapt(self, result, context):
        from datetime import UTC, datetime
        from src.core_intelligence.models import Observation
        from src.providers.adapters import AdapterResult
        value = result.value if isinstance(result.value, dict) else {'value': result.value}; ident = str(value.get('signature', context.execution_id))
        return AdapterResult(self.metadata.adapter_id, (Observation(f'solana:{ident}', 'solana', ident, 'json-rpc', datetime.now(UTC), datetime.now(UTC), 'solana-adapter-1', ident, value),), result.provenance)
