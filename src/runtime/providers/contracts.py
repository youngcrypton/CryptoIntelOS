from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Protocol
class ProviderStatus(StrEnum): UNKNOWN="unknown"; HEALTHY="healthy"; DEGRADED="degraded"; UNAVAILABLE="unavailable"
@dataclass(frozen=True, slots=True)
class ProviderCapability: name: str; version: str = "1.0"
@dataclass(frozen=True, slots=True)
class ProviderHealth: status: ProviderStatus; checked_at: datetime = field(default_factory=lambda: datetime.now(UTC)); detail: str = ""
@dataclass(frozen=True, slots=True)
class ProviderDescriptor: provider_id: str; name: str; version: str = "1.0"; capabilities: tuple[ProviderCapability, ...] = ()
@dataclass(frozen=True, slots=True)
class ProviderResult: provider_id: str; success: bool; value: object = None; error: str | None = None
class RateLimiter(Protocol):
    def acquire(self, provider_id: str) -> bool: ...
class BackoffStrategy(Protocol):
    def delay_seconds(self, attempt: int) -> float: ...
class CircuitBreaker(Protocol):
    def allow(self, provider_id: str) -> bool: ...
class ProviderNegotiation(Protocol):
    def negotiate(self, descriptor: ProviderDescriptor, required: tuple[ProviderCapability, ...]) -> bool: ...
class ProviderRegistry:
    def __init__(self): self._providers: dict[str, ProviderDescriptor] = {}
    def register(self, descriptor: ProviderDescriptor) -> None: self._providers[descriptor.provider_id] = descriptor
    def get(self, provider_id: str) -> ProviderDescriptor | None: return self._providers.get(provider_id)
    def all(self) -> tuple[ProviderDescriptor, ...]: return tuple(self._providers.values())
class CapabilityRegistry:
    def supports(self, descriptor: ProviderDescriptor, required: tuple[ProviderCapability, ...]) -> bool: return all(item in descriptor.capabilities for item in required)
class ProviderMonitor:
    def __init__(self): self._health: dict[str, ProviderHealth] = {}
    def record(self, provider_id: str, health: ProviderHealth) -> None: self._health[provider_id] = health
    def health(self, provider_id: str) -> ProviderHealth | None: return self._health.get(provider_id)
