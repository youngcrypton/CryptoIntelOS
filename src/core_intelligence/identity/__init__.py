"""Source-agnostic canonical identity contracts."""
from .entity import Entity
from .entity_type import EntityType
from .identity import Identity
from .identifier import Identifier
from .identifier_type import IdentifierType
from .relationship import LegacyIdentityRelationship
from .relationship_type import RelationshipType
from .identity_context import IdentityContext
from .identity_registry import IdentityRegistry

__all__ = ["Entity", "EntityType", "Identity", "Identifier", "IdentifierType", "LegacyIdentityRelationship", "RelationshipType", "IdentityContext", "IdentityRegistry"]
