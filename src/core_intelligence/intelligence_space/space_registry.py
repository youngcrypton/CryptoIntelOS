"""Protocol for future Intelligence Space runtime providers."""
from typing import Protocol
from uuid import UUID
from .space import Space
from .space_snapshot import SpaceSnapshot

class SpaceRegistry(Protocol):
    def register(self, space: Space) -> UUID: ...
    def get(self, space_id: UUID) -> Space | None: ...
    def create_snapshot(self, space_id: UUID) -> SpaceSnapshot: ...
