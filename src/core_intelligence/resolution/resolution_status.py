"""Lifecycle statuses for resolution decisions."""
from enum import StrEnum

class ResolutionStatus(StrEnum):
    PENDING = "pending"
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    REJECTED = "rejected"
    MANUAL_REVIEW = "manual_review"
