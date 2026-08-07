from dataclasses import dataclass

from src.platform_sdk import RuntimeFacade
from src.platform_sdk.runtime import CanonicalOutput
from src.runtime.engine import ExecutionContext, ExecutionResult


@dataclass(frozen=True, slots=True)
class TwitterRuntimeIntegration:
    """Delegate canonical Twitter outputs to the existing Runtime façade."""

    facade: RuntimeFacade

    def integrate(
        self, output: CanonicalOutput, context: ExecutionContext
    ) -> ExecutionResult:
        return self.facade.integrate(output, context)
