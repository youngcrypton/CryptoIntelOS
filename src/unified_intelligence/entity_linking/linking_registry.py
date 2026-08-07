from .exceptions import DuplicateLinkingStrategyError, LinkingStrategyNotFoundError
from .linking_strategy import EntityLinkingStrategy


class LinkingRegistry:
    def __init__(self) -> None:
        self._strategies: dict[str, EntityLinkingStrategy] = {}

    def register(self, strategy: EntityLinkingStrategy) -> None:
        if strategy.strategy_id in self._strategies:
            raise DuplicateLinkingStrategyError(strategy.strategy_id)
        self._strategies[strategy.strategy_id] = strategy

    def get(self, strategy_id: str) -> EntityLinkingStrategy:
        try:
            return self._strategies[strategy_id]
        except KeyError as error:
            raise LinkingStrategyNotFoundError(strategy_id) from error

    def all(self) -> tuple[EntityLinkingStrategy, ...]:
        return tuple(self._strategies.values())
