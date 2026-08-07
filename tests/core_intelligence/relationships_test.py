from dataclasses import FrozenInstanceError, asdict
from datetime import UTC, datetime
from uuid import UUID

import pytest

from src.core_intelligence.identity import Entity, EntityType, RelationshipType
from src.core_intelligence.relationships import (
    Relationship,
    RelationshipCategory,
    RelationshipContext,
    RelationshipDirection,
    RelationshipMetadata,
    RelationshipStrength,
)

def test_relationship_construction_and_integrity() -> None:
    source = Entity(entity_type=EntityType.ORGANIZATION)
    target = Entity(entity_type=EntityType.PROJECT)
    context = RelationshipContext("github", collector="collector", analyzer="analyzer")
    relationship = Relationship(source_entity=source, target_entity=target, relationship_type=RelationshipType.MAINTAINS, category=RelationshipCategory.TECHNICAL, direction=RelationshipDirection.DIRECTED, strength=RelationshipStrength.STRONG, confidence=0.9, provenance=context, evidence=("evidence-1",), created_at=datetime.now(UTC), metadata=RelationshipMetadata(tags=("core",)))
    assert isinstance(relationship.relationship_id, UUID)
    assert relationship.source_entity is source and relationship.target_entity is target
    assert asdict(relationship)["metadata"]["tags"] == ("core",)

@pytest.mark.parametrize("value", list(RelationshipCategory))
def test_categories_are_enumerated(value: RelationshipCategory) -> None:
    assert isinstance(value.value, str)

@pytest.mark.parametrize("value", list(RelationshipDirection))
def test_directions_are_enumerated(value: RelationshipDirection) -> None:
    assert isinstance(value.value, str)

def test_contracts_are_immutable() -> None:
    metadata = RelationshipMetadata()
    with pytest.raises(FrozenInstanceError):
        metadata.version = "2"
