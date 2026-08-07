from .distribution_context import DistributionContext
from .distribution_plan import DistributionPlan
from .distribution_registry import DistributionRegistry
from .distribution_result import DistributionResult
from .distribution_strategy import DistributionStrategy


class DistributionEngine:
    """Coordinates delivery through pluggable strategies and providers."""

    def __init__(self, registry: DistributionRegistry) -> None:
        self._registry = registry

    def distribute(
        self,
        plan: DistributionPlan,
        context: DistributionContext,
        strategy: DistributionStrategy,
    ) -> tuple[DistributionResult, ...]:
        return strategy.distribute(plan, context, self._registry)
