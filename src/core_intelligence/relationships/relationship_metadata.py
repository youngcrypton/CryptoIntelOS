"""Immutable metadata attached to a relationship."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class RelationshipMetadata:
    discovery_source: str | None = None
    evidence_count: int | None = None
    tags: tuple[str, ...] = ()
    labels: tuple[str, ...] = ()
    version: str | None = None
