from dataclasses import dataclass
from .automation_priority import AutomationPriority
from .automation_rule import AutomationRule

@dataclass(frozen=True, slots=True)
class AutomationPolicy:
    name: str
    rules: tuple[AutomationRule, ...] = ()
    default_priority: AutomationPriority = AutomationPriority.NORMAL
    enabled: bool = True
