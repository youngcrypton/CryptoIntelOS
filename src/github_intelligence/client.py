"""HTTP request preparation for the GitHub Intelligence foundation."""

from collections.abc import Mapping
from urllib.parse import urljoin
from urllib.request import Request

from .auth import GitHubAuthenticator, PersonalAccessTokenAuth
from .config import GitHubConfig
from .rate_limiter import RateLimiter


class GitHubClient:
    """Prepare authenticated GitHub requests without repository logic."""

    def __init__(
        self,
        config: GitHubConfig | None = None,
        authenticator: GitHubAuthenticator | None = None,
    ) -> None:
        """Initialize a client with configuration and optional PAT auth."""

        self.config = config or GitHubConfig()
        self.rate_limiter = RateLimiter()
        self.authenticator = authenticator
        if self.authenticator is None and self.config.token:
            self.authenticator = PersonalAccessTokenAuth(self.config.token)

    def prepare_request(
        self,
        path: str,
        method: str = "GET",
        headers: Mapping[str, str] | None = None,
    ) -> Request:
        """Build an authenticated standard-library HTTP request.

        This method does not open a connection or perform an API call.
        """

        request_headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": self.config.user_agent,
        }
        if self.authenticator is not None:
            request_headers.update(self.authenticator.headers())
        if headers:
            request_headers.update(headers)

        return Request(
            url=self.build_url(path),
            method=method,
            headers=request_headers,
        )

    def build_url(self, path: str) -> str:
        """Resolve a relative API path against the configured base URL."""

        return urljoin(f"{self.config.api_base_url.rstrip('/')}/", path.lstrip('/'))
