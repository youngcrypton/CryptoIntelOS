from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True, slots=True)
class AutomationCondition:
    field: str
    operator: str
    value: Any = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
