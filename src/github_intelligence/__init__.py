"""GitHub Intelligence foundation primitives."""

from .client import GitHubClient
from .commit_analyzer import CommitAnalyzer, CommitIntelligence
from .config import GitHubConfig
from .contributor_analyzer import ContributorAnalyzer, ContributorIntelligence
from .dependency_analyzer import DependencyAnalyzer, DependencyIntelligence
from .models import Commit, Contributor, Organization, Release, Repository
from .release_analyzer import ReleaseAnalyzer, ReleaseIntelligence
from .repository_scoring import (
    RepositoryScore,
    RepositoryScoringEngine,
    ScoreExplanation,
)

__all__ = [
    "Commit",
    "CommitAnalyzer",
    "CommitIntelligence",
    "Contributor",
    "ContributorAnalyzer",
    "ContributorIntelligence",
    "DependencyAnalyzer",
    "DependencyIntelligence",
    "GitHubClient",
    "GitHubConfig",
    "Organization",
    "Release",
    "ReleaseAnalyzer",
    "ReleaseIntelligence",
    "Repository",
    "RepositoryScore",
    "RepositoryScoringEngine",
    "ScoreExplanation",
]
