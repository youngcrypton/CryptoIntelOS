"""Declarative future retention policy contract."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MemoryPolicy:
    name: str
    version: str = "1"
    retention_period: str | None = None
    metadata: tuple[tuple[str, str], ...] = ()
