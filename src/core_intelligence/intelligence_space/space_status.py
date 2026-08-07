"""Runtime lifecycle states for Intelligence Space objects."""
from enum import StrEnum

class SpaceStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    REMOVED = "removed"
