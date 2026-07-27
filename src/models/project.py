from dataclasses import dataclass


@dataclass
class Project:
    """Represents a monitored crypto project."""

    id: int
    name: str
    website: str
    blockchain: str
    category: str
    status: str