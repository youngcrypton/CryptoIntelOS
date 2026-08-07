"""Canonical relationship contract."""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from src.core_intelligence.identity.entity import Entity
from src.core_intelligence.identity.relationship_type import RelationshipType
from .relationship_category import RelationshipCategory
from .relationship_context import RelationshipContext
from .relationship_direction import RelationshipDirection
from .relationship_metadata import RelationshipMetadata
from .relationship_strength import RelationshipStrength

@dataclass(frozen=True, slots=True, kw_only=True)
class Relationship:
    relationship_id: UUID = field(default_factory=uuid4)
    source_entity: Entity | UUID
    target_entity: Entity | UUID
    relationship_type: RelationshipType
    category: RelationshipCategory
    direction: RelationshipDirection
    strength: RelationshipStrength = RelationshipStrength.UNKNOWN
    confidence: float | None = None
    provenance: RelationshipContext | None = None
    evidence: tuple[str, ...] = ()
    created_at: datetime | None = None
    metadata: RelationshipMetadata = field(default_factory=RelationshipMetadata)
