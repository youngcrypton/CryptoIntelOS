from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
@dataclass(frozen=True, slots=True, kw_only=True)
class PolicyDecision:
    policy_reference: UUID | str
    applied_rules: tuple[UUID | str, ...] = ()
    outcome: str | None = None
    confidence: float | None = None
    timestamp: datetime | None = None
    decision_id: UUID = field(default_factory=uuid4)
