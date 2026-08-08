"""Legacy persistence/application signal DTO.

Deprecated: adapt to ``src.core_intelligence.models.Signal`` before Runtime use.
"""

__deprecated__ = True

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class LegacyIntelligenceSignal:
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


IntelligenceSignal = LegacyIntelligenceSignal
