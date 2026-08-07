"""Real-world entity contract."""
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .entity_type import EntityType
from .identity import Identity

@dataclass(frozen=True, slots=True)
class Entity:
    entity_id: UUID = field(default_factory=uuid4)
    entity_type: EntityType = EntityType.UNKNOWN
    identity: Identity | None = None
