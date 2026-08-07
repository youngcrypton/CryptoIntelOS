"""Immutable provenance context for relationships."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class RelationshipContext:
    source: str
    collector: str | None = None
    analyzer: str | None = None
    timestamp: datetime | None = None
    policy_version: str | None = None
