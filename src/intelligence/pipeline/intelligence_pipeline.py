"""
Intelligence Pipeline

Executes intelligence analyzers and builds a
LivingIntelligenceProfile.

Responsibilities
----------------
- Execute analyzers
- Catch analyzer exceptions
- Merge AnalyzerResults
- Record execution metrics
- Keep the intelligence process resilient

The pipeline owns execution.

The engine owns orchestration.
"""

from __future__ import annotations

import time
from typing import Any, Dict, Iterable

from src.intelligence.analyzers.base_analyzer import BaseAnalyzer
from src.intelligence.models.living_intelligence_profile import (
    LivingIntelligenceProfile,
)
from src.intelligence.models.analyzer_result import AnalyzerResult


class IntelligencePipeline:
    """
    Executes analyzers against a repository.
    """

    def __init__(
        self,
        analyzers: Iterable[BaseAnalyzer],
    ) -> None:

        self.analyzers = list(analyzers)

    def execute(
        self,
        repository: Dict[str, Any],
    ) -> LivingIntelligenceProfile:
        """
        Execute every analyzer and return a populated
        LivingIntelligenceProfile.
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

            start = time.perf_counter()

            try:

                result = analyzer.analyze(repository)

            except Exception as ex:

                duration = time.perf_counter() - start

                result = AnalyzerResult(
                    analyzer=analyzer.name,
                    section=analyzer.section,
                    success=False,
                    errors=[str(ex)],
                    duration=duration,
                )

            else:

                result.duration = (
                    time.perf_counter() - start
                )

            profile.merge(result)

        return profile