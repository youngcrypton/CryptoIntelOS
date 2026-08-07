"""Immutable provenance context for canonical identity data."""
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class IdentityContext:
    source: str
    observed_at: datetime | None = None
    source_record_id: str | None = None
    metadata: tuple[tuple[str, str], ...] = ()
