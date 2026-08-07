from dataclasses import dataclass, field
from datetime import datetime, timezone

from .distribution_message import DistributionMessage
from .distribution_priority import DistributionPriority
from .distribution_target import DistributionTarget


@dataclass(frozen=True, slots=True)
class DistributionRequest:
    request_id: str
    message: DistributionMessage
    target: DistributionTarget
    priority: DistributionPriority = DistributionPriority.NORMAL
    scheduled_for: datetime | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
