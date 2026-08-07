"""Assessment currently being calculated."""
from dataclasses import dataclass, field
from src.core_intelligence import Assessment
from .space_status import SpaceStatus

@dataclass(slots=True)
class ActiveAssessment:
    assessment: Assessment
    status: SpaceStatus = SpaceStatus.PENDING
    metadata: dict[str, str] = field(default_factory=dict)
