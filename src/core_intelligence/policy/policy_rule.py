from dataclasses import dataclass, field
from uuid import UUID, uuid4
@dataclass(frozen=True, slots=True, kw_only=True)
class PolicyRule:
    policy_reference: UUID | str
    rule_name: str
    priority: int
    conditions: tuple[str, ...] = ()
    outcome: str | None = None
    explanation: str | None = None
    rule_id: UUID = field(default_factory=uuid4)
