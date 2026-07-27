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