from src.models.project_intelligence_profile import (
    ProjectIntelligenceProfile,
)
from src.models.intelligence_signal import (
    IntelligenceSignal,
)


class DiscoveryEngine:
    """
    Builds and maintains intelligence profiles for discovered projects.
    """

    def __init__(self):
        self.projects = {}

    def process_signal(self, signal: IntelligenceSignal):
        """
        Process a newly discovered intelligence signal.
        """

        if signal.project_name is None:
            return

        # Create a new profile if it doesn't exist
        if signal.project_name not in self.projects:
            self.projects[signal.project_name] = (
                ProjectIntelligenceProfile(
                    project_name=signal.project_name,
                    blockchain=signal.blockchain or "Unknown",
                    category=signal.category or "Unknown",
                )
            )

        profile = self.projects[signal.project_name]

        # Add the new signal
        profile.add_signal(signal)

        print(
            f"[Discovery Engine] "
            f"{profile.project_name} "
            f"({profile.signal_count} signals)"
        )

    def get_profile(self, project_name: str):
        """
        Retrieve a project's intelligence profile.
        """
        return self.projects.get(project_name)

    def list_profiles(self):
        """
        Return all discovered project profiles.
        """
        return list(self.projects.values())


discovery_engine = DiscoveryEngine()