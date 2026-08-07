from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from .distribution_policy import DistributionPolicy
from .distribution_request import DistributionRequest


@dataclass(frozen=True, slots=True)
class DistributionPlan:
    plan_id: str = field(default_factory=lambda: str(uuid4()))
    requests: tuple[DistributionRequest, ...] = ()
    policy: DistributionPolicy = field(default_factory=DistributionPolicy)
    strategy_name: str = "immediate"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
