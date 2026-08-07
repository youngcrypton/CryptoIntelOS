"""Transient runtime working-memory contract."""
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .space_context import SpaceContext

@dataclass(slots=True)
class Space:
    execution_context: SpaceContext
    space_id: UUID = field(default_factory=uuid4)
    active_objects: list[object] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
