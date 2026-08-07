from typing import Protocol

from .distribution_context import DistributionContext
from .distribution_plan import DistributionPlan
from .distribution_registry import DistributionRegistry
from .distribution_result import DistributionResult


class DistributionStrategy(Protocol):
    def distribute(
        self,
        plan: DistributionPlan,
        context: DistributionContext,
        registry: DistributionRegistry,
    ) -> tuple[DistributionResult, ...]: ...
