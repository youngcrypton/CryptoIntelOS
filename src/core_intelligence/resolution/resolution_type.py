"""Canonical resolution operation types."""
from enum import StrEnum

class ResolutionType(StrEnum):
    ENTITY = "entity"
    IDENTIFIER = "identifier"
    RELATIONSHIP = "relationship"
    EVIDENCE = "evidence"
    FINDING = "finding"
    ASSESSMENT = "assessment"
    SIGNAL = "signal"
