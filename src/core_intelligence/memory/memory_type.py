"""Canonical memory object types."""
from enum import StrEnum

class MemoryType(StrEnum):
    OBSERVATION = "observation"
    EVIDENCE = "evidence"
    ENTITY = "entity"
    IDENTITY = "identity"
    RELATIONSHIP = "relationship"
    RESOLUTION_DECISION = "resolution_decision"
    FINDING = "finding"
    ASSESSMENT = "assessment"
    SIGNAL = "signal"
