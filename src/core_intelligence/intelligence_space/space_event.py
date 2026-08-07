"""Change event emitted within Intelligence Space."""
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

class SpaceEventType(StrEnum):
    OBJECT_ADDED = "object_added"
    OBJECT_REMOVED = "object_removed"
    OBJECT_UPDATED = "object_updated"
    SNAPSHOT_CREATED = "snapshot_created"
    EXECUTION_STARTED = "execution_started"
    EXECUTION_FINISHED = "execution_finished"

@dataclass(frozen=True, slots=True)
class SpaceEvent:
    event_id: UUID
    space_id: UUID
    event_type: SpaceEventType
    timestamp: datetime
    object_reference: str | None = None
    metadata: tuple[tuple[str, str], ...] = ()
