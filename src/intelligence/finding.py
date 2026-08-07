"""Legacy finding DTO.

Deprecated: use ``src.core_intelligence.models.Finding`` at subsystem boundaries.
This DTO remains for backwards compatibility with the legacy rule engine.
"""

__deprecated__ = True

from dataclasses import dataclass


@dataclass
class Finding:
    """
    Represents one intelligence finding produced by a rule.
    """

    title: str

    summary: str

    severity: str

    confidence: int

    evidence: str = ""

    source: str = ""
