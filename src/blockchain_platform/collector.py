from typing import Protocol

from src.platform_sdk import SourceCollector


class BlockchainCollector(SourceCollector, Protocol):
    """SDK collector contract for future blockchain data providers."""
