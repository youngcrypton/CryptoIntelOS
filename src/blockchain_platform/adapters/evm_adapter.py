from typing import Protocol

from .blockchain_adapter import BlockchainAdapter


class EVMAdapter(BlockchainAdapter, Protocol):
    """Contract stub for adapters targeting EVM-compatible chains."""
