"""Immutable blockchain infrastructure contracts."""

from dataclasses import dataclass

from .capabilities import BlockchainCapability
from .transport import TransportType


@dataclass(frozen=True, slots=True)
class ChainCapability:
    capability: BlockchainCapability
    enabled: bool = True
    description: str | None = None


@dataclass(frozen=True, slots=True)
class ChainEndpoint:
    endpoint_id: str
    chain_id: str
    url: str
    transport: TransportType
    priority: int = 0
    enabled: bool = True


@dataclass(frozen=True, slots=True)
class ChainMetadata:
    chain_id: str
    network_type: str
    native_currency: str
    capabilities: tuple[ChainCapability, ...] = ()
    block_explorer_url: str | None = None


@dataclass(frozen=True, slots=True)
class Blockchain:
    chain_id: str
    name: str
    slug: str
    metadata: ChainMetadata
    endpoints: tuple[ChainEndpoint, ...] = ()
