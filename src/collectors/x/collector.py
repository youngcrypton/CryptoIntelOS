from src.collectors.base_collector import BaseCollector
from src.collectors.x.provider import x_provider

from src.models.collector_result import CollectorResult


class XCollector(BaseCollector):
    """
    Collects X profile intelligence.
    """

    name = "X Collector"

    def collect(self, project):

        profile = x_provider.get_profile(project)

        if profile is None:
            return None

        print(f"✓ {self.name}: {project.name}")

        return CollectorResult(
            project=project.name,
            collector=self.name,
            signal_type="X Profile",
            title="X Profile Collected",
            summary="Profile collected successfully.",
            confidence=100,
            evidence="Mock provider returned profile.",
            payload=profile,
        )


x_collector = XCollector()