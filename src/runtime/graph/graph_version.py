from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True, slots=True)
class GraphVersion:
    version: str
    created_at: datetime
    memory_version: str | None = None
    supersedes: str | None = None
