from typing import Protocol
from .automation_context import AutomationContext
from .automation_plan import AutomationPlan
from .automation_policy import AutomationPolicy

class AutomationStrategy(Protocol):
    def decide(self, context: AutomationContext, policy: AutomationPolicy) -> tuple[AutomationPlan, ...]: ...
