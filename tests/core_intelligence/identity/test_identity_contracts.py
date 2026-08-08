from dataclasses import FrozenInstanceError, asdict
from datetime import UTC, datetime
from typing import get_type_hints
from uuid import UUID

import pytest

from src.core_intelligence.identity import (
    Entity,
    EntityType,
    Identifier,
    IdentifierType,
    Identity,
    IdentityContext,
    RelationshipType,
)
from src.core_intelligence.relationships import Relationship, RelationshipCategory, RelationshipDirection


def test_constructs_entity_with_canonical_identity() -> None:
    context = IdentityContext(
        source="github",
        observed_at=datetime(2026, 8, 7, tzinfo=UTC),
        source_record_id="repository:123",
        metadata=(("collector", "github"),),
    )
    identifier = Identifier(
        value="123",
        identifier_type=IdentifierType.GITHUB_REPOSITORY_ID,
        context=context,
    )
    identity = Identity(canonical_name="example/project", identifiers=(identifier,))
    entity = Entity(entity_type=EntityType.REPOSITORY, identity=identity)

    assert isinstance(entity.entity_id, UUID)
    assert entity.identity is identity
    assert entity.identity.identifiers == (identifier,)


@pytest.mark.parametrize(
    "instance, attribute, value",
    [
        (Entity(), "entity_type", EntityType.PROJECT),
        (Identity(), "canonical_name", "changed"),
        (
            Identifier("example.org", IdentifierType.WEBSITE_DOMAIN),
            "value",
            "changed.org",
        ),
        (IdentityContext("website"), "source", "changed"),
    ],
)
def test_contracts_are_immutable(instance: object, attribute: str, value: object) -> None:
    with pytest.raises(FrozenInstanceError):
        setattr(instance, attribute, value)


def test_dataclass_contracts_support_standard_serialization() -> None:
    entity = Entity(
        entity_type=EntityType.PROJECT,
        identity=Identity(
            canonical_name="Example",
            identifiers=(Identifier("example.org", IdentifierType.WEBSITE_DOMAIN),),
        ),
    )

    serialized = asdict(entity)

    assert serialized["entity_type"] is EntityType.PROJECT
    assert serialized["identity"]["canonical_name"] == "Example"


def test_relationship_preserves_typed_endpoints() -> None:
    organization = Entity(entity_type=EntityType.ORGANIZATION)
    project = Entity(entity_type=EntityType.PROJECT)
    relationship = Relationship(
        source_entity=organization,
        target_entity=project.entity_id,
        relationship_type=RelationshipType.FOUNDED,
        category=RelationshipCategory.ORGANIZATIONAL,
        direction=RelationshipDirection.DIRECTED,
    )

    assert relationship.source_entity is organization
    assert relationship.target_entity == project.entity_id
    assert relationship.source_entity != relationship.target_entity
    assert get_type_hints(Relationship)["source_entity"] == Entity | UUID
