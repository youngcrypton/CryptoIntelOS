from dataclasses import dataclass


@dataclass
class SourceDefinition:
    """
    Represents one intelligence source definition.
    """

    id: str

    name: str

    category: str

    description: str

    collector: str

    enabled: bool

    priority: int

    evidence_weight: int

    authentication: bool

    access_method: str

    rate_limit: int

    update_interval: int

    supported_chains: list

    tags: list