"""Immutable execution metadata for Intelligence Space."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class SpaceContext:
    execution_id: str
    pipeline_stage: str
    source: str
    started_at: datetime
    metadata: tuple[tuple[str, str], ...] = ()
