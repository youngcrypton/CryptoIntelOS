from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Mapping, Protocol

class ConnectorError(Exception): pass
class ConnectorUnavailableError(ConnectorError): pass
class ConnectorConfigurationError(ConnectorError): pass
class ConnectorHealthStatus(StrEnum): UNKNOWN="unknown"; HEALTHY="healthy"; DEGRADED="degraded"; UNAVAILABLE="unavailable"
@dataclass(frozen=True, slots=True)
class ConnectorCapability: name: str; version: str = "1.0"
@dataclass(frozen=True, slots=True)
class ConnectorMetadata: connector_id: str; name: str; version: str = "1.0"; capabilities: tuple[ConnectorCapability, ...] = ()
@dataclass(frozen=True, slots=True)
class ConnectorContext: correlation_id: str; execution_id: str; metadata: tuple[tuple[str, str], ...] = ()
@dataclass(frozen=True, slots=True)
class ConnectorPolicy: timeout_seconds: float = 30.0; metadata: tuple[tuple[str, str], ...] = ()
@dataclass(frozen=True, slots=True)
class ConnectorHealth: status: ConnectorHealthStatus; checked_at: datetime = field(default_factory=lambda: datetime.now(UTC)); detail: str = ""
@dataclass(frozen=True, slots=True)
class ConnectorResult: connector_id: str; success: bool; payload: Any = None; error: str | None = None; metadata: Mapping[str, Any] = field(default_factory=dict)
class Connector(Protocol):
    @property
    def metadata(self) -> ConnectorMetadata: ...
    def request(self, operation: str, context: ConnectorContext, policy: ConnectorPolicy) -> ConnectorResult: ...
class ConnectorRegistry:
    def __init__(self): self._connectors: dict[str, Connector] = {}
    def register(self, connector: Connector) -> None: self._connectors[connector.metadata.connector_id] = connector
    def get(self, connector_id: str) -> Connector | None: return self._connectors.get(connector_id)
    def all(self) -> tuple[Connector, ...]: return tuple(self._connectors.values())
