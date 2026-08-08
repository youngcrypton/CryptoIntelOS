from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Protocol
from src.providers.providers import ProviderResult
from src.core_intelligence.models import Assessment, Evidence, Finding, Observation, Signal
class AdapterError(Exception): pass
class AdapterValidationError(AdapterError): pass
@dataclass(frozen=True, slots=True)
class AdapterMetadata: adapter_id: str; name: str; version: str = "1.0"
@dataclass(frozen=True, slots=True)
class AdapterContext: execution_id: str; source: str; metadata: tuple[tuple[str, str], ...] = ()
@dataclass(frozen=True, slots=True)
class AdapterResult: adapter_id: str; objects: tuple[Observation | Evidence | Finding | Assessment | Signal, ...]; provenance: tuple[tuple[str, str], ...] = ()
@dataclass(frozen=True, slots=True)
class AdapterStrategy: strategy_id: str
class Adapter(Protocol):
    @property
    def metadata(self) -> AdapterMetadata: ...
    def adapt(self, result: ProviderResult, context: AdapterContext) -> AdapterResult: ...
class AdapterRegistry:
    def __init__(self): self._adapters: dict[str, Adapter] = {}
    def register(self, adapter: Adapter) -> None: self._adapters[adapter.metadata.adapter_id] = adapter
    def get(self, adapter_id: str) -> Adapter | None: return self._adapters.get(adapter_id)
    def all(self) -> tuple[Adapter, ...]: return tuple(self._adapters.values())
