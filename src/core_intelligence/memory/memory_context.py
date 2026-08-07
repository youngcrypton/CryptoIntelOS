"""Immutable provenance context for memory records."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class MemoryContext:
    source: str
    recorded_at: datetime | None = None
    collector: str | None = None
    policy_version: str | None = None
