"""Canonical reference from one memory object to another."""
from dataclasses import dataclass
from uuid import UUID
from .memory_type import MemoryType

@dataclass(frozen=True, slots=True)
class MemoryReference:
    object_id: UUID
    memory_type: MemoryType
    version: int | None = None
