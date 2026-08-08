"""Deprecated identity-edge DTO.

Use ``src.core_intelligence.relationships.Relationship`` for canonical relationships.
"""
__deprecated__ = True
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .entity import Entity
from .relationship_type import RelationshipType
from .identity_context import IdentityContext

@dataclass(frozen=True, slots=True)
class LegacyIdentityRelationship:
    subject: Entity | UUID
    object: Entity | UUID
    relationship_type: RelationshipType
    relationship_id: UUID = field(default_factory=uuid4)
    context: IdentityContext | None = None


Relationship = LegacyIdentityRelationship
