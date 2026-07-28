from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class IntelligenceSignal:
    """
    Represents a single intelligence signal discovered by a collector.
    """

    signal_type: str
    source: str
    project_name: Optional[str]
    blockchain: Optional[str]
    category: Optional[str]
    title: str
    description: str
    url: str
    confidence: float
    timestamp: datetime