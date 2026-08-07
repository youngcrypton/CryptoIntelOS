from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping

class AutomationActionType(str, Enum):
    NOTIFY = "notify"; WATCH = "watch"; ARCHIVE = "archive"; ESCALATE = "escalate"
    SCHEDULE = "schedule"; EXPORT = "export"; WEBHOOK = "webhook"; DASHBOARD_PIN = "dashboard_pin"

@dataclass(frozen=True, slots=True)
class AutomationAction:
    action_type: AutomationActionType | str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    rationale: str | None = None
