from dataclasses import dataclass
from datetime import datetime


@dataclass
class IntelligenceEvent:
    """
    Standard intelligence object shared across CryptoIntel OS.
    """

    source: str
    category: str
    title: str
    summary: str
    confidence: float
    url: str
    timestamp: datetime