from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True, slots=True)
class PolicyVersion:
    version: str
    effective_at: datetime | None = None
    supersedes: str | None = None
