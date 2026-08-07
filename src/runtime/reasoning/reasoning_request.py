from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .reasoning_type import ReasoningType
@dataclass(frozen=True, slots=True, kw_only=True)
class ReasoningRequest:
    reasoning_type: ReasoningType
    inputs: tuple[object, ...]
    request_id: UUID = field(default_factory=uuid4)
    instructions: str | None = None
    metadata: tuple[tuple[str,str], ...] = ()
