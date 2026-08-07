"""Relationship currently under analysis."""
from dataclasses import dataclass, field
from src.core_intelligence.relationships import Relationship
from .space_status import SpaceStatus

@dataclass(slots=True)
class ActiveRelationship:
    relationship: Relationship
    status: SpaceStatus = SpaceStatus.PENDING
    metadata: dict[str, str] = field(default_factory=dict)
