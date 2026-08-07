from dataclasses import dataclass, field
from uuid import UUID, uuid4
@dataclass(frozen=True, slots=True, kw_only=True)
class PolicyOverride:
    policy_reference: UUID | str
    owner_reference: str
    values: tuple[tuple[str,str], ...] = ()
    reason: str | None = None
    override_id: UUID = field(default_factory=uuid4)
