from dataclasses import dataclass, field
from typing import Any, Mapping

from .distribution_channel import DistributionChannel


@dataclass(frozen=True, slots=True)
class DistributionTarget:
    target_id: str
    channel: DistributionChannel
    address: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)
