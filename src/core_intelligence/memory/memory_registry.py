"""Protocol for future memory storage providers."""
from typing import Protocol
from uuid import UUID
from .memory_object import MemoryObject
from .memory_snapshot import MemorySnapshot

class MemoryRegistry(Protocol):
    def append(self, memory_object: MemoryObject) -> UUID: ...
    def get(self, object_id: UUID, version: int | None = None) -> MemoryObject | None: ...
    def snapshot(self, snapshot_id: str) -> MemorySnapshot | None: ...
