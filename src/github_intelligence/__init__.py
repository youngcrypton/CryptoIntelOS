"""GitHub Intelligence foundation primitives."""

from .client import GitHubClient
from .commit_analyzer import CommitAnalyzer, CommitIntelligence
from .config import GitHubConfig
from .contributor_analyzer import ContributorAnalyzer, ContributorIntelligence
from .dependency_analyzer import DependencyAnalyzer, DependencyIntelligence
from .models import Commit, Contributor, Organization, Release, Repository
from .organization_analyzer import OrganizationAnalyzer, OrganizationIntelligence
from .release_analyzer import ReleaseAnalyzer, ReleaseIntelligence
from .repository_scoring import (
    RepositoryScore,
    RepositoryScoringEngine,
    ScoreExplanation,
)
from .signal_engine import (
    GitHubIntelligenceSignal,
    GitHubSignalEngine,
    GitHubSignalRule,
    SignalRuleMatch,
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
    "GitHubIntelligenceSignal",
    "GitHubSignalEngine",
    "GitHubSignalRule",
    "Organization",
    "OrganizationAnalyzer",
    "OrganizationIntelligence",
    "Release",
    "ReleaseAnalyzer",
    "ReleaseIntelligence",
    "Repository",
    "RepositoryScore",
    "RepositoryScoringEngine",
    "ScoreExplanation",
    "SignalRuleMatch",
]
