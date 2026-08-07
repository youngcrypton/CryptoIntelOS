"""Immutable execution provenance for resolution."""
from dataclasses import dataclass
from datetime import datetime
from .resolution_policy import ResolutionPolicy

@dataclass(frozen=True, slots=True)
class ResolutionContext:
    execution_id: str
    source: str
    policy: ResolutionPolicy
    timestamp: datetime | None = None
