from .blockchain_adapter import BlockchainAdapter
from .exceptions import AdapterNotFoundError, DuplicateAdapterError


class AdapterRegistry:
    """Ordered registry of blockchain adapter protocol implementations."""

    def __init__(self) -> None:
        self._adapters: dict[str, BlockchainAdapter] = {}

    def register(self, adapter: BlockchainAdapter) -> None:
        if adapter.adapter_id in self._adapters:
            raise DuplicateAdapterError(adapter.adapter_id)
        self._adapters[adapter.adapter_id] = adapter

    def get(self, adapter_id: str) -> BlockchainAdapter:
        try:
            return self._adapters[adapter_id]
        except KeyError as error:
            raise AdapterNotFoundError(adapter_id) from error

    def all(self) -> tuple[BlockchainAdapter, ...]:
        return tuple(self._adapters.values())
