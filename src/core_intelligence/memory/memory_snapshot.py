"""Immutable point-in-time view of memory."""
from dataclasses import dataclass
from datetime import datetime
from .memory_reference import MemoryReference

@dataclass(frozen=True, slots=True)
class MemorySnapshot:
    snapshot_id: str
    captured_at: datetime
    objects: tuple[MemoryReference, ...] = ()
