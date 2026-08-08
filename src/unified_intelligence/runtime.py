from dataclasses import dataclass

from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult

from .entity_linking.identity_bundle import IdentityBundle
from .runtime_projection import project_evidence_bundle, project_identity_bundle


@dataclass(frozen=True, slots=True)
class UnifiedRuntimeIntegration:
    facade: RuntimeFacade

    def integrate(self, bundle: IdentityBundle | object, context: ExecutionContext) -> ExecutionResult:
        if hasattr(bundle, "identity") and hasattr(bundle, "groups"):
            return self.facade.integrate(project_evidence_bundle(bundle, context), context)
        return self.facade.integrate(project_identity_bundle(bundle, context), context)
