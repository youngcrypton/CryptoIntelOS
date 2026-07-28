from datetime import datetime

from src.collectors.base.base_collector import BaseCollector
from src.models.intelligence_event import IntelligenceEvent


class ProjectDiscoveryCollector(BaseCollector):
    """
    Simulates discovery of a new crypto project.
    """

    def __init__(self):
        super().__init__("Project Discovery")

    def collect(self):

        return {
            "title": "Example AI Protocol",
            "summary": "A new AI infrastructure protocol has been discovered.",
            "category": "Project Discovery",
            "source": "Simulation",
            "url": "https://example.xyz"
        }

    def normalize(self, data):

        return IntelligenceEvent(
            source=data["source"],
            category=data["category"],
            title=data["title"],
            summary=data["summary"],
            confidence=95.0,
            url=data["url"],
            timestamp=datetime.utcnow()
        )


collector = ProjectDiscoveryCollector()