from dataclasses import dataclass
from datetime import datetime
from .automation_status import AutomationStatus

@dataclass(frozen=True, slots=True)
class AutomationExecution:
    execution_id: str
    plan_id: str
    status: AutomationStatus = AutomationStatus.PROPOSED
    started_at: datetime | None = None
    completed_at: datetime | None = None
