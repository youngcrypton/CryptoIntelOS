"""Entity currently under analysis."""
from dataclasses import dataclass, field
from src.core_intelligence.identity import Entity
from .space_status import SpaceStatus

@dataclass(slots=True)
class ActiveEntity:
    entity: Entity
    status: SpaceStatus = SpaceStatus.PENDING
    metadata: dict[str, str] = field(default_factory=dict)
