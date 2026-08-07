from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DistributionChannel:
    name: str
    channel_type: str
