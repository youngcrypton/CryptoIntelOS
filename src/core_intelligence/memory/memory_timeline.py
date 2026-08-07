"""Chronological, append-only memory history."""
from dataclasses import dataclass
from .memory_reference import MemoryReference
from .memory_version import MemoryVersion

@dataclass(frozen=True, slots=True)
class MemoryTimeline:
    object_id: str
    versions: tuple[MemoryVersion, ...] = ()
    references: tuple[MemoryReference, ...] = ()
