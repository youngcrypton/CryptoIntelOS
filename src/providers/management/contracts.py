from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol
from src.providers.connectors import Connector, ConnectorContext, ConnectorPolicy
from src.providers.providers import Provider, ProviderContext, ProviderPolicy, ProviderHealth, ProviderStatus
from src.providers.adapters import Adapter, AdapterContext, AdapterResult
class FailoverPolicy(Protocol):
    def candidates(self, providers: tuple[Provider, ...]) -> tuple[Provider, ...]: ...
@dataclass(frozen=True, slots=True)
class RateLimitPolicy: requests: int; per_seconds: float
@dataclass(frozen=True, slots=True)
class RetryPolicy: max_attempts: int = 3
@dataclass(frozen=True, slots=True)
class CircuitBreaker: failure_threshold: int = 5; reset_seconds: float = 60.0
@dataclass(frozen=True, slots=True)
class ProviderMetrics: provider_id: str; requests: int = 0; successes: int = 0; failures: int = 0; total_duration_ms: float = 0.0
@dataclass(frozen=True, slots=True)
class ProviderStatistics: metrics: tuple[ProviderMetrics, ...] = (); generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
class CapabilityNegotiator:
    def supports(self, available: tuple[str, ...], required: tuple[str, ...]) -> bool: return set(required).issubset(available)
class ProviderSelector:
    def select(self, providers: tuple[Provider, ...]) -> Provider | None: return providers[0] if providers else None
class HealthManager:
    def __init__(self): self._health: dict[str, ProviderHealth] = {}
    def record(self, provider_id: str, health: ProviderHealth) -> None: self._health[provider_id] = health
    def available(self, provider_id: str) -> bool: return self._health.get(provider_id, ProviderHealth(ProviderStatus.UNKNOWN)).status in {ProviderStatus.HEALTHY, ProviderStatus.DEGRADED}
@dataclass(frozen=True, slots=True)
class ProviderExecution:
    connector_id: str; provider_id: str; adapter_id: str; result: AdapterResult
class ProviderManager:
    """Deterministically orchestrate Connector -> Provider -> Adapter only."""
    def execute(self, connector: Connector, provider: Provider, adapter: Adapter, operation: str, execution_id: str, correlation_id: str) -> ProviderExecution:
        connector_result = connector.request(operation, ConnectorContext(correlation_id, execution_id), ConnectorPolicy())
        provider_result = provider.normalize(connector_result, ProviderContext(execution_id, correlation_id), ProviderPolicy())
        adapted = adapter.adapt(provider_result, AdapterContext(execution_id, provider.metadata.source))
        return ProviderExecution(connector.metadata.connector_id, provider.metadata.provider_id, adapter.metadata.adapter_id, adapted)
