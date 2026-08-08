from dataclasses import dataclass

from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult

from .entity_linking.identity_bundle import IdentityBundle
from .runtime_projection import project_identity_bundle


@dataclass(frozen=True, slots=True)
class UnifiedRuntimeIntegration:
    facade: RuntimeFacade

    def integrate(self, bundle: IdentityBundle, context: ExecutionContext) -> ExecutionResult:
        return self.facade.integrate(project_identity_bundle(bundle, context), context)
