from typing import Protocol

from .evm_adapter import EVMAdapter


class EthereumAdapter(EVMAdapter, Protocol):
    """Contract stub for future Ethereum provider adapters."""
