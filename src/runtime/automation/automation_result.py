from dataclasses import dataclass
from .automation_plan import AutomationPlan
from .automation_status import AutomationStatus

@dataclass(frozen=True, slots=True)
class AutomationResult:
    status: AutomationStatus
    plans: tuple[AutomationPlan, ...] = ()
    explanation: str = ""
