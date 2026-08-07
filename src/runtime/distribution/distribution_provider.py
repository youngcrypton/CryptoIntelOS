from typing import Protocol

from .distribution_context import DistributionContext
from .distribution_request import DistributionRequest
from .distribution_result import DistributionResult


class DistributionProvider(Protocol):
    def deliver(
        self,
        request: DistributionRequest,
        context: DistributionContext,
    ) -> DistributionResult: ...
