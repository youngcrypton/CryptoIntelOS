from .exceptions import DuplicateFusionStrategyError, FusionStrategyNotFoundError
from .fusion_strategy import AssessmentFusionStrategy


class FusionRegistry:
    def __init__(self) -> None:
        self._strategies: dict[str, AssessmentFusionStrategy] = {}

    def register(self, strategy: AssessmentFusionStrategy) -> None:
        if strategy.strategy_id in self._strategies:
            raise DuplicateFusionStrategyError(strategy.strategy_id)
        self._strategies[strategy.strategy_id] = strategy

    def get(self, strategy_id: str) -> AssessmentFusionStrategy:
        try:
            return self._strategies[strategy_id]
        except KeyError as error:
            raise FusionStrategyNotFoundError(strategy_id) from error

    def all(self) -> tuple[AssessmentFusionStrategy, ...]:
        return tuple(self._strategies.values())
