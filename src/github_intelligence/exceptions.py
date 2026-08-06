"""Exceptions raised by GitHub Intelligence components."""


class GitHubAPIError(Exception):
    """Base error for GitHub API communication and response failures."""


class AuthenticationError(GitHubAPIError):
    """Raised when GitHub authentication is invalid or unavailable."""


class RateLimitExceeded(GitHubAPIError):
    """Raised when the configured GitHub request budget is exhausted."""


class RepositoryNotFound(GitHubAPIError):
    """Raised when a requested repository cannot be found."""
