from .exceptions import DuplicateProfileStrategyError, ProfileStrategyNotFoundError
from .profile_strategy import ProfileStrategy


class ProfileRegistry:
    def __init__(self) -> None:
        self._strategies: dict[str, ProfileStrategy] = {}

    def register(self, strategy: ProfileStrategy) -> None:
        if strategy.strategy_id in self._strategies:
            raise DuplicateProfileStrategyError(strategy.strategy_id)
        self._strategies[strategy.strategy_id] = strategy

    def get(self, strategy_id: str) -> ProfileStrategy:
        try:
            return self._strategies[strategy_id]
        except KeyError as error:
            raise ProfileStrategyNotFoundError(strategy_id) from error

    def all(self) -> tuple[ProfileStrategy, ...]:
        return tuple(self._strategies.values())
