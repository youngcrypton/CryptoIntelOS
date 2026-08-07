"""Protocol for future relationship registry implementations."""
from typing import Protocol
from uuid import UUID
from .relationship import Relationship

class RelationshipRegistry(Protocol):
    def register(self, relationship: Relationship) -> UUID: ...
    def get(self, relationship_id: UUID) -> Relationship | None: ...
