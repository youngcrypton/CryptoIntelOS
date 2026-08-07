from .exceptions import DuplicateProviderError, ProviderNotFoundError
from .provider import BlockchainProvider


class ProviderRegistry:
    """Ordered registry of provider protocol implementations."""

    def __init__(self) -> None:
        self._providers: dict[str, BlockchainProvider] = {}

    def register(self, provider: BlockchainProvider) -> None:
        provider_id = provider.metadata().provider_id
        if provider_id in self._providers:
            raise DuplicateProviderError(provider_id)
        self._providers[provider_id] = provider

    def get(self, provider_id: str) -> BlockchainProvider:
        try:
            return self._providers[provider_id]
        except KeyError as error:
            raise ProviderNotFoundError(provider_id) from error

    def all(self) -> tuple[BlockchainProvider, ...]:
        return tuple(self._providers.values())
