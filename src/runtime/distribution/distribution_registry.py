from typing import Protocol

from .distribution_provider import DistributionProvider


class DistributionRegistry(Protocol):
    def register(self, name: str, provider: DistributionProvider) -> None: ...

    def get(self, name: str) -> DistributionProvider | None: ...
