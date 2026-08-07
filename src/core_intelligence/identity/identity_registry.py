"""Protocol for future identity registration implementations."""
from typing import Protocol
from uuid import UUID
from .entity import Entity
from .identity import Identity

class IdentityRegistry(Protocol):
    def register(self, entity: Entity) -> Identity: ...
    def get(self, entity_id: UUID) -> Entity | None: ...
