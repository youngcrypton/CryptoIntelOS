from typing import Protocol, TypeVar

from .onchain_type import OnChainType


OnChainModel = TypeVar("OnChainModel")


class OnChainRegistry(Protocol[OnChainModel]):
    """Protocol-only registry boundary for canonical on-chain entities."""

    def register(self, value: OnChainModel) -> None: ...

    def get(self, identifier: str) -> OnChainModel: ...

    def supports(self, entity_type: OnChainType) -> bool: ...
