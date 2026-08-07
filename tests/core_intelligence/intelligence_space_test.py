from dataclasses import asdict
from datetime import UTC, datetime
from typing import get_type_hints
from uuid import uuid4

from src.core_intelligence.identity import Entity, EntityType
from src.core_intelligence.intelligence_space import (
    ActiveEntity,
    Space,
    SpaceContext,
    SpaceEvent,
    SpaceEventType,
    SpaceRegistry,
    SpaceSnapshot,
    SpaceStatus,
    Workspace,
)

def test_space_and_workspace_construction() -> None:
    context = SpaceContext("execution-1", "analysis", "github", datetime.now(UTC))
    active = ActiveEntity(Entity(entity_type=EntityType.PROJECT))
    space = Space(context, active_objects=[active])
    workspace = Workspace("project-analysis", spaces=[space])
    active.status = SpaceStatus.ACTIVE
    assert workspace.spaces[0].active_objects[0].status is SpaceStatus.ACTIVE

def test_context_and_snapshot_integrity() -> None:
    context = SpaceContext("execution-1", "collection", "web", datetime.now(UTC))
    space = Space(context)
    snapshot = SpaceSnapshot(uuid4(), space.space_id, datetime.now(UTC), tuple(space.active_objects))
    assert snapshot.space_id == space.space_id
    assert asdict(snapshot)["active_objects"] == ()

def test_event_serialization_and_typing() -> None:
    space_id = uuid4()
    event = SpaceEvent(uuid4(), space_id, SpaceEventType.EXECUTION_STARTED, datetime.now(UTC))
    assert asdict(event)["event_type"] is SpaceEventType.EXECUTION_STARTED
    assert get_type_hints(Space)["execution_context"] is SpaceContext

def test_registry_is_protocol_contract() -> None:
    assert "register" in SpaceRegistry.__dict__
    assert "create_snapshot" in SpaceRegistry.__dict__
