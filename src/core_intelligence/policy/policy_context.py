from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True, slots=True)
class PolicyContext:
    execution_id: str
    subsystem: str
    source: str
    timestamp: datetime | None = None
    metadata: tuple[tuple[str,str], ...] = ()
