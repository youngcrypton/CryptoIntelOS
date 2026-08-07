from enum import StrEnum
from typing import Protocol


class TransportType(StrEnum):
    """Transport families that a chain endpoint may describe."""

    RPC = "rpc"
    REST = "rest"
    GRAPHQL = "graphql"
    WEBSOCKET = "websocket"


class BlockchainTransport(Protocol):
    """Descriptive transport contract with no network behavior."""

    @property
    def transport_type(self) -> TransportType: ...

    @property
    def endpoint(self) -> str: ...
