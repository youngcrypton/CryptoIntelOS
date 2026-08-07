from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from .correlation_context import CorrelationContext
from .correlation_type import CorrelationType
@dataclass(frozen=True, slots=True, kw_only=True)
class Correlation:
    correlation_id: UUID = field(default_factory=uuid4)
    correlation_type: CorrelationType
    participating_entities: tuple[object, ...] = ()
    participating_evidence: tuple[object, ...] = ()
    participating_relationships: tuple[object, ...] = ()
    confidence: float | None = None
    explanation: str | None = None
    provenance: CorrelationContext | None = None
    timestamp: datetime | None = None
