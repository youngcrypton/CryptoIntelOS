"""Request to resolve canonical objects."""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from .resolution_type import ResolutionType

@dataclass(frozen=True, slots=True, kw_only=True)
class ResolutionRequest:
    request_id: UUID = field(default_factory=uuid4)
    resolution_type: ResolutionType
    submitted_objects: tuple[object, ...]
    created_at: datetime | None = None
    metadata: tuple[tuple[str, str], ...] = ()
