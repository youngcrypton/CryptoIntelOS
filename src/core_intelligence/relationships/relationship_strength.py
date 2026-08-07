"""Normalized relationship strength levels."""
from enum import StrEnum

class RelationshipStrength(StrEnum):
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"
    UNKNOWN = "unknown"
