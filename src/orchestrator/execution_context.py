"""Deprecated collector execution DTO.

Use ``src.runtime.engine.ExecutionContext`` at execution boundaries.
"""

__deprecated__ = True

from dataclasses import dataclass
from datetime import datetime


@dataclass
class LegacyCollectorExecutionContext:
    """
    Runtime information for a collector execution.
    """

    collector_name: str

    started_at: datetime

    finished_at: datetime | None = None

    success: bool = False

    error: str = ""


ExecutionContext = LegacyCollectorExecutionContext
