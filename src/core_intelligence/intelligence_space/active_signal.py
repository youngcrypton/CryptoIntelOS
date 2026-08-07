"""Signal awaiting publication."""
from dataclasses import dataclass, field
from src.core_intelligence import Signal
from .space_status import SpaceStatus

@dataclass(slots=True)
class ActiveSignal:
    signal: Signal
    status: SpaceStatus = SpaceStatus.PENDING
    metadata: dict[str, str] = field(default_factory=dict)
