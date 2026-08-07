"""Canonical relationship categories."""
from enum import StrEnum

class RelationshipCategory(StrEnum):
    STRUCTURAL = "structural"
    ORGANIZATIONAL = "organizational"
    FINANCIAL = "financial"
    TECHNICAL = "technical"
    SOCIAL = "social"
    COMMUNITY = "community"
    GOVERNANCE = "governance"
    SECURITY = "security"
    INFRASTRUCTURE = "infrastructure"
    UNKNOWN = "unknown"
