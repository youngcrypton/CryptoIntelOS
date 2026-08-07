"""Lifecycle status for memory records."""
from enum import StrEnum

class MemoryStatus(StrEnum):
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    RETIRED = "retired"
    REVOKED = "revoked"
