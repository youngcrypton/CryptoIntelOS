from dataclasses import dataclass

from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult

from .entity_linking.identity_bundle import IdentityBundle


@dataclass(frozen=True, slots=True)
class UnifiedRuntimeIntegration:
    facade: RuntimeFacade

    def integrate(self, bundle: IdentityBundle, context: ExecutionContext) -> ExecutionResult:
        return self.facade.integrate(bundle, context)  # type: ignore[arg-type]
