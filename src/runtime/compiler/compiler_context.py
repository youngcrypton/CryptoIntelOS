from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True, slots=True)
class CompilerContext:
    execution_id: str
    source: str
    timestamp: datetime | None = None
    metadata: tuple[tuple[str, str], ...] = ()
