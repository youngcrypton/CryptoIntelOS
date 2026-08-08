"""Legacy persistence DTO; canonical projects use Identity ``EntityType.PROJECT``."""

__deprecated__ = True

from dataclasses import dataclass


@dataclass
class LegacyProject:
    """Represents a monitored crypto project."""

    id: int
    name: str
    website: str
    blockchain: str
    category: str
    status: str


Project = LegacyProject
