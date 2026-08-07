from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True, slots=True)
class ReasoningContext:
    execution_id: str
    source: str
    timestamp: datetime
    metadata: tuple[tuple[str,str], ...] = ()
