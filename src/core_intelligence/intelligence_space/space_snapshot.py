"""Immutable point-in-time view of runtime state."""
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True, slots=True)
class SpaceSnapshot:
    snapshot_id: UUID
    space_id: UUID
    captured_at: datetime
    active_objects: tuple[object, ...] = ()
    metadata: tuple[tuple[str, str], ...] = ()
