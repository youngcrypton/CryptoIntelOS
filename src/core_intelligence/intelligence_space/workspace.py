"""Scoped execution workspace contract."""
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .space import Space

@dataclass(slots=True)
class Workspace:
    name: str
    workspace_id: UUID = field(default_factory=uuid4)
    project_reference: str | None = None
    spaces: list[Space] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
