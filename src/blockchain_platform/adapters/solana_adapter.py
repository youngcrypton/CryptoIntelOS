from typing import Protocol

from .blockchain_adapter import BlockchainAdapter


class SolanaAdapter(BlockchainAdapter, Protocol):
    """Contract stub for future Solana provider adapters."""
