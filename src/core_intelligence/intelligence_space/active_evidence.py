"""Evidence currently being processed."""
from dataclasses import dataclass, field
from src.core_intelligence import Evidence
from .space_status import SpaceStatus

@dataclass(slots=True)
class ActiveEvidence:
    evidence: Evidence
    status: SpaceStatus = SpaceStatus.PENDING
    metadata: dict[str, str] = field(default_factory=dict)
