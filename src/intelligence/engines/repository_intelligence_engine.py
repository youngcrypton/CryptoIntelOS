"""
Repository Intelligence Engine

Coordinates repository intelligence analyzers and builds a
LivingIntelligenceProfile.

Responsibilities
----------------
- Create a LivingIntelligenceProfile
- Execute registered analyzers
- Merge AnalyzerResults
- Return the completed intelligence profile

The engine never performs analysis itself.
"""

from typing import Any, Dict, List

from src.intelligence.analyzers.base_analyzer import BaseAnalyzer
from src.intelligence.models.living_intelligence_profile import (
    LivingIntelligenceProfile,
)


class RepositoryIntelligenceEngine:
    """
    Orchestrates repository intelligence analyzers.
    """

    def __init__(self) -> None:
        self.analyzers: List[BaseAnalyzer] = []

    def register_analyzer(self, analyzer: BaseAnalyzer) -> None:
        """
        Register an analyzer with the engine.
        """

        self.analyzers.append(analyzer)

    def register_analyzers(
        self,
        analyzers: List[BaseAnalyzer],
    ) -> None:
        """
        Register multiple analyzers.
        """

        self.analyzers.extend(analyzers)

    def analyze(
        self,
        repository: Dict[str, Any],
    ) -> LivingIntelligenceProfile:
        """
        Execute every registered analyzer against a repository.

        Parameters
        ----------
        repository : dict
            Repository discovered by the Discovery Engine.

        Returns
        -------
        LivingIntelligenceProfile
        """

        profile = LivingIntelligenceProfile()

        profile.repository = repository

        profile.discovery_evidence = repository.get(
            "discovery_evidence",
            [],
        )

        profile.discovery_history.append(
            {
                "event": "repository_discovered",
                "repository": repository.get("full_name"),
            }
        )

        for analyzer in self.analyzers:

            result = analyzer.analyze(repository)

            profile.merge(result)

        return profile