from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from .policy_scope import PolicyScope
from .policy_status import PolicyStatus
from .policy_type import PolicyType
from .policy_version import PolicyVersion
@dataclass(frozen=True, slots=True, kw_only=True)
class Policy:
    policy_id: UUID = field(default_factory=uuid4)
    policy_name: str
    policy_type: PolicyType
    policy_version: PolicyVersion
    description: str | None = None
    scope: PolicyScope = PolicyScope.PLATFORM
    status: PolicyStatus = PolicyStatus.DRAFT
    metadata: tuple[tuple[str,str], ...] = ()
    created_at: datetime | None = None
