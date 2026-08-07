"""Append-only envelope for any canonical intelligence object."""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from .memory_context import MemoryContext
from .memory_status import MemoryStatus
from .memory_type import MemoryType
from .memory_version import MemoryVersion

@dataclass(frozen=True, slots=True, kw_only=True)
class MemoryObject:
    object_id: UUID = field(default_factory=uuid4)
    memory_type: MemoryType
    payload: object
    version: MemoryVersion
    context: MemoryContext | None = None
    status: MemoryStatus = MemoryStatus.ACTIVE
    recorded_at: datetime | None = None
