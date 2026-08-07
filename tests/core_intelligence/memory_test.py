from dataclasses import FrozenInstanceError, asdict
from datetime import UTC, datetime
from uuid import uuid4
import pytest
from src.core_intelligence.memory import *

def test_memory_construction_and_serialization() -> None:
    version = MemoryVersion(1, datetime.now(UTC))
    obj = MemoryObject(memory_type=MemoryType.ENTITY, payload={"name": "Example"}, version=version)
    assert obj.version.version == 1
    assert asdict(obj)["memory_type"] is MemoryType.ENTITY

def test_timeline_and_snapshot_integrity() -> None:
    oid = uuid4()
    ref = MemoryReference(oid, MemoryType.ENTITY, 1)
    timeline = MemoryTimeline(str(oid), (MemoryVersion(1),), (ref,))
    snapshot = MemorySnapshot("snap-1", datetime.now(UTC), (ref,))
    assert timeline.references[0] == snapshot.objects[0]

def test_contracts_are_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        MemoryVersion(1).version = 2
