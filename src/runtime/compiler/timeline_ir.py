from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True, slots=True)
class TimelineIR:
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    sequence: int | None = None
