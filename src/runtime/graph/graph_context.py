from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True, slots=True)
class GraphContext:
    execution_id: str
    source_memory_version: str
    timestamp: datetime
    metadata: tuple[tuple[str, str], ...] = ()
