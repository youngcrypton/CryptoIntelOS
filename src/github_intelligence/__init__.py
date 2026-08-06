"""GitHub Intelligence foundation primitives."""

from .client import GitHubClient
from .config import GitHubConfig
from .models import Commit, Contributor, Organization, Release, Repository

__all__ = [
    "Commit",
    "Contributor",
    "GitHubClient",
    "GitHubConfig",
    "Organization",
    "Release",
    "Repository",
]
