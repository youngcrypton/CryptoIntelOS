from collections.abc import Mapping, Sequence
from typing import Any, Protocol

from .provider_metadata import ProviderMetadata


ProviderRecord = Mapping[str, Any]


class BlockchainProvider(Protocol):
    """Provider-neutral raw blockchain data acquisition contract."""

    def metadata(self) -> ProviderMetadata: ...

    def discover_wallet(self, identifier: str) -> ProviderRecord | None: ...

    def discover_transactions(self, identifier: str) -> Sequence[ProviderRecord]: ...

    def discover_contracts(self, identifier: str) -> Sequence[ProviderRecord]: ...

    def discover_tokens(self, identifier: str) -> Sequence[ProviderRecord]: ...

    def discover_nfts(self, identifier: str) -> Sequence[ProviderRecord]: ...

    def discover_protocols(self, identifier: str) -> Sequence[ProviderRecord]: ...

    def discover_governance(self, identifier: str) -> Sequence[ProviderRecord]: ...
