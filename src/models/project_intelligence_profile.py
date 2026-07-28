from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from src.models.intelligence_signal import IntelligenceSignal


@dataclass
class ProjectIntelligenceProfile:
    """
    Living intelligence profile for a discovered project.
    """

    project_name: str
    blockchain: str = "Unknown"
    category: str = "Unknown"

    confidence_score: float = 0.0
    risk_score: float = 0.0

    first_seen: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)

    signals: List[IntelligenceSignal] = field(default_factory=list)

    website: str = ""
    github: str = ""
    twitter: str = ""
    discord: str = ""
    telegram: str = ""
    whitepaper: str = ""
    documentation: str = ""

    ai_summary: str = ""

    def add_signal(self, signal: IntelligenceSignal):

        self.signals.append(signal)

        self.last_updated = datetime.utcnow()

    @property
    def signal_count(self):

        return len(self.signals)