from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Protocol
from src.providers.connectors import ConnectorContext, ConnectorResult
class ProviderError(Exception): pass
class ProviderNotFoundError(ProviderError): pass
class ProviderConfigurationError(ProviderError): pass
class ProviderStatus(StrEnum): UNKNOWN="unknown"; HEALTHY="healthy"; DEGRADED="degraded"; UNAVAILABLE="unavailable"
@dataclass(frozen=True, slots=True)
class ProviderMetadata: provider_id: str; name: str; version: str = "1.0"; source: str = "external"
@dataclass(frozen=True, slots=True)
class ProviderContext: execution_id: str; correlation_id: str; metadata: tuple[tuple[str, str], ...] = ()
@dataclass(frozen=True, slots=True)
class ProviderPolicy: timeout_seconds: float = 30.0; preserve_raw_payload: bool = True
@dataclass(frozen=True, slots=True)
class ProviderHealth: status: ProviderStatus; checked_at: datetime = field(default_factory=lambda: datetime.now(UTC)); detail: str = ""
@dataclass(frozen=True, slots=True)
class ProviderResult: provider_id: str; success: bool; value: Any = None; error: str | None = None; provenance: tuple[tuple[str, str], ...] = ()
@dataclass(frozen=True, slots=True)
class ProviderStrategy: strategy_id: str
class Provider(Protocol):
    @property
    def metadata(self) -> ProviderMetadata: ...
    def normalize(self, result: ConnectorResult, context: ProviderContext, policy: ProviderPolicy) -> ProviderResult: ...
class ProviderRegistry:
    def __init__(self): self._providers: dict[str, Provider] = {}
    def register(self, provider: Provider) -> None: self._providers[provider.metadata.provider_id] = provider
    def get(self, provider_id: str) -> Provider | None: return self._providers.get(provider_id)
    def all(self) -> tuple[Provider, ...]: return tuple(self._providers.values())
