from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True, slots=True)
class ExecutionContext:
    execution_id: str
    runtime_version: str
    started_at: datetime
    metadata: tuple[tuple[str,str], ...] = ()
