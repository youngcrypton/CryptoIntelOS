from dataclasses import dataclass

from .distribution_priority import DistributionPriority


@dataclass(frozen=True, slots=True)
class DistributionPolicy:
    max_attempts: int = 1
    batch_size: int | None = None
    default_priority: DistributionPriority = DistributionPriority.NORMAL
    allow_partial_delivery: bool = True
