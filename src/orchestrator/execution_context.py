from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExecutionContext:
    """
    Runtime information for a collector execution.
    """

    collector_name: str

    started_at: datetime

    finished_at: datetime | None = None

    success: bool = False

    error: str = ""