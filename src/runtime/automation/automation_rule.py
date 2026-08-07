from dataclasses import dataclass
from .automation_condition import AutomationCondition
from .automation_trigger import AutomationTrigger
from .automation_action import AutomationAction

@dataclass(frozen=True, slots=True)
class AutomationRule:
    name: str
    trigger: AutomationTrigger
    conditions: tuple[AutomationCondition, ...] = ()
    actions: tuple[AutomationAction, ...] = ()
    explanation: str = ""
