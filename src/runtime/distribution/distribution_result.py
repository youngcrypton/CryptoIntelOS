from dataclasses import dataclass, field
from datetime import datetime, timezone

from .distribution_status import DistributionStatus


@dataclass(frozen=True, slots=True)
class DistributionResult:
    request_id: str
    status: DistributionStatus
    provider_name: str | None = None
    attempt_count: int = 0
    detail: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
