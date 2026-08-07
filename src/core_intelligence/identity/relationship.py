"""Typed relationships between canonical entities."""
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .entity import Entity
from .relationship_type import RelationshipType
from .identity_context import IdentityContext

@dataclass(frozen=True, slots=True)
class Relationship:
    subject: Entity | UUID
    object: Entity | UUID
    relationship_type: RelationshipType
    relationship_id: UUID = field(default_factory=uuid4)
    context: IdentityContext | None = None
