"""Coordinator for repository metadata and activity analysis."""

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from ..commit_analyzer import CommitIntelligence
from ..contributor_analyzer import ContributorIntelligence
from ..dependency_analyzer import DependencyIntelligence
from ..models import Repository
from ..release_analyzer import ReleaseIntelligence
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
    contributor_intelligence: list[ContributorIntelligence] = field(default_factory=list)
    commit_intelligence: CommitIntelligence | None = None
    release_intelligence: ReleaseIntelligence | None = None
    dependency_intelligence: DependencyIntelligence | None = None


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
        contributors: list[ContributorIntelligence] | None = None,
        commits: CommitIntelligence | None = None,
        releases: ReleaseIntelligence | None = None,
        dependencies: DependencyIntelligence | None = None,
    ) -> RepositoryAnalysis:
        """Analyze a repository using metadata supplied by a caller or API layer."""

        return RepositoryAnalysis(
            repository=repository,
            technologies=self.technology_detector.detect(repository, metadata),
            activity_metrics=self.activity_analyzer.analyze(repository, metadata),
            metadata=self.metadata_extractor.extract(repository, metadata),
            contributor_intelligence=list(contributors or []),
            commit_intelligence=commits,
            release_intelligence=releases,
            dependency_intelligence=dependencies,
        )
