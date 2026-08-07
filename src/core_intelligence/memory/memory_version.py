"""Immutable revision marker for a memory object."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class MemoryVersion:
    version: int
    created_at: datetime | None = None
    supersedes: int | None = None
