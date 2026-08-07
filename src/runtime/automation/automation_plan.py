from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4
from .automation_action import AutomationAction
from .automation_priority import AutomationPriority

@dataclass(frozen=True, slots=True)
class AutomationPlan:
    plan_id: str = field(default_factory=lambda: str(uuid4()))
    actions: tuple[AutomationAction, ...] = ()
    priority: AutomationPriority = AutomationPriority.NORMAL
    explanation: str = ""
    supporting_reasoning: tuple[str, ...] = ()
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
