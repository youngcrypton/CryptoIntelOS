from .exceptions import BlockchainNotFoundError, DuplicateBlockchainError
from .models import Blockchain


class BlockchainRegistry:
    """In-memory registry of immutable blockchain definitions."""

    def __init__(self) -> None:
        self._chains: dict[str, Blockchain] = {}

    def register(self, blockchain: Blockchain) -> None:
        if blockchain.chain_id in self._chains:
            raise DuplicateBlockchainError(blockchain.chain_id)
        self._chains[blockchain.chain_id] = blockchain

    def get(self, chain_id: str) -> Blockchain:
        try:
            return self._chains[chain_id]
        except KeyError as error:
            raise BlockchainNotFoundError(chain_id) from error

    def all(self) -> tuple[Blockchain, ...]:
        return tuple(self._chains.values())
