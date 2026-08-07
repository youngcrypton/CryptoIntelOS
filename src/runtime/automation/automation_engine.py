from .automation_context import AutomationContext
from .automation_policy import AutomationPolicy
from .automation_registry import AutomationRegistry
from .automation_result import AutomationResult
from .automation_status import AutomationStatus

class AutomationEngine:
    """Coordinates deterministic decisions; it never executes actions."""
    def __init__(self, registry: AutomationRegistry): self._registry = registry
    def decide(self, context: AutomationContext, policy: AutomationPolicy, strategy_name: str) -> AutomationResult:
        if not policy.enabled: return AutomationResult(AutomationStatus.REJECTED, explanation="Policy disabled")
        strategy = self._registry.get(strategy_name)
        if strategy is None: raise KeyError(strategy_name)
        return AutomationResult(AutomationStatus.PROPOSED, strategy.decide(context, policy))
