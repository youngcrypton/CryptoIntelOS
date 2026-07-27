from dataclasses import dataclass
from typing import Any


@dataclass
class CollectorResult:
    """
    Standard result returned by every collector.
    """

    project: str

    collector: str

    signal_type: str

    title: str

    summary: str

    confidence: int

    evidence: str

    payload: Any = None