"""Coordinator for repository metadata and activity analysis."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from ..models import Repository
from .activity_analyzer import ActivityAnalyzer
from .metadata_extractor import MetadataExtractor
from .technology_detector import TechnologyDetector


@dataclass(frozen=True)
class RepositoryAnalysis:
    """Structured repository analysis without summaries or intelligence scores."""

    repository: Repository
    technologies: list[str]
    activity_metrics: dict[str, int | float | str | None]
    metadata: dict[str, object]


class RepositoryAnalyzer:
    """Coordinate independent repository analysis components."""

    def __init__(
        self,
        technology_detector: TechnologyDetector | None = None,
        activity_analyzer: ActivityAnalyzer | None = None,
        metadata_extractor: MetadataExtractor | None = None,
    ) -> None:
        """Initialize analysis components, allowing focused substitutions."""

        self.technology_detector = technology_detector or TechnologyDetector()
        self.activity_analyzer = activity_analyzer or ActivityAnalyzer()
        self.metadata_extractor = metadata_extractor or MetadataExtractor()

    def analyze(
        self,
        repository: Repository,
        metadata: Mapping[str, Any] | None = None,
    ) -> RepositoryAnalysis:
        """Analyze a repository using metadata supplied by a caller or API layer."""

        return RepositoryAnalysis(
            repository=repository,
            technologies=self.technology_detector.detect(repository, metadata),
            activity_metrics=self.activity_analyzer.analyze(repository, metadata),
            metadata=self.metadata_extractor.extract(repository, metadata),
        )
