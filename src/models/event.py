from dataclasses import dataclass


@dataclass
class Event:
    """Represents an intelligence event."""

    id: int

    project: str

    source: str

    signal_type: str

    title: str

    summary: str

    priority: str

    confidence: int

    evidence: str

    created_at: str