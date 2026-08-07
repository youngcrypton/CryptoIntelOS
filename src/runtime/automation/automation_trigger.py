from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True, slots=True)
class AutomationTrigger:
    name: str
    event_type: str
    attributes: Mapping[str, Any] = field(default_factory=dict)
