"""Configuration for GitHub Intelligence HTTP clients."""

from dataclasses import dataclass


@dataclass(frozen=True)
class GitHubConfig:
    """HTTP and authentication settings for the GitHub API."""

    api_base_url: str = "https://api.github.com"
    token: str | None = None
    timeout: float = 10.0
    retries: int = 3
    user_agent: str = "CryptoIntelOS-GitHubIntelligence/0.1"
