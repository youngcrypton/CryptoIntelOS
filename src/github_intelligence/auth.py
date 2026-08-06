"""Authentication strategies for GitHub requests."""

from dataclasses import dataclass
from typing import Protocol


class GitHubAuthenticator(Protocol):
    """Protocol implemented by GitHub authentication strategies."""

    def headers(self) -> dict[str, str]:
        """Return request headers required by the strategy."""


@dataclass(frozen=True)
class PersonalAccessTokenAuth:
    """Authenticate GitHub API requests with a personal access token."""

    token: str

    def headers(self) -> dict[str, str]:
        """Return the bearer authorization header for the token."""

        return {"Authorization": f"Bearer {self.token}"}
