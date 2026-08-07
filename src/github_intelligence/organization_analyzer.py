"""GitHub organization metadata collection and intelligence modeling."""

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

from .client import GitHubClient


@dataclass(frozen=True)
class OrganizationIntelligence:
    """Structured intelligence collected from a GitHub organization profile."""

    id: int
    login: str
    name: str | None
    verified: bool
    repository_count: int
    public_member_count: int | None
    followers: int
    following: int
    description: str | None
    website: str | None
    location: str | None
    created_at: str | None
    updated_at: str | None
    html_url: str | None
    avatar_url: str | None
    email: str | None
    twitter_username: str | None


class OrganizationAnalyzer:
    """Fetch and normalize public GitHub organization intelligence."""

    def __init__(
        self,
        client: GitHubClient | None = None,
        opener: Callable[..., Any] | None = None,
    ) -> None:
        """Initialize with reusable HTTP dependencies."""

        self.client = client or GitHubClient()
        self._opener = opener or urlopen

    def analyze(self, login: str) -> OrganizationIntelligence:
        """Fetch an organization profile and return normalized intelligence."""

        normalized_login = self._normalize_login(login)
        metadata, _ = self._fetch(
            self.client.prepare_request(f"/orgs/{normalized_login}")
        )
        public_member_count = self._fetch_public_member_count(normalized_login)

        return OrganizationIntelligence(
            id=self._integer(metadata.get("id")),
            login=str(metadata.get("login") or normalized_login),
            name=self._optional_string(metadata.get("name")),
            verified=bool(
                metadata.get("is_verified", metadata.get("verified", False))
            ),
            repository_count=self._integer(metadata.get("public_repos")),
            public_member_count=public_member_count,
            followers=self._integer(metadata.get("followers")),
            following=self._integer(metadata.get("following")),
            description=self._optional_string(metadata.get("description")),
            website=self._optional_string(metadata.get("blog")),
            location=self._optional_string(metadata.get("location")),
            created_at=self._optional_string(metadata.get("created_at")),
            updated_at=self._optional_string(metadata.get("updated_at")),
            html_url=self._optional_string(metadata.get("html_url")),
            avatar_url=self._optional_string(metadata.get("avatar_url")),
            email=self._optional_string(metadata.get("email")),
            twitter_username=self._optional_string(metadata.get("twitter_username")),
        )

    def _fetch_public_member_count(self, login: str) -> int | None:
        """Return the public member count, or ``None`` when unavailable."""

        request = self.client.prepare_request(
            f"/orgs/{login}/public_members?per_page=1"
        )
        try:
            payload, headers = self._fetch(request)
        except HTTPError as error:
            if error.code in {403, 404}:
                return None
            raise

        link_header = headers.get("Link", "")
        last_page = self._last_page(link_header)
        if last_page is not None:
            return last_page
        return len(payload) if isinstance(payload, list) else None

    def _fetch(self, request: Request) -> tuple[Any, Mapping[str, str]]:
        """Open and decode one GitHub API request."""

        self.client.rate_limiter.ensure_available()
        with self._opener(request, timeout=self.client.config.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            headers = response.headers
        self._update_rate_limit(headers)
        return payload, headers

    def _update_rate_limit(self, headers: Mapping[str, str]) -> None:
        """Update the shared client rate-limit state when headers are present."""

        remaining = headers.get("X-RateLimit-Remaining")
        used = headers.get("X-RateLimit-Used")
        reset = headers.get("X-RateLimit-Reset")
        if remaining is not None and used is not None and reset is not None:
            self.client.rate_limiter.update(
                self._integer(remaining),
                self._integer(used),
                self._integer(reset),
            )

    @staticmethod
    def _last_page(link_header: str) -> int | None:
        """Extract the final page number from a GitHub Link header."""

        for link in link_header.split(","):
            if 'rel="last"' not in link:
                continue
            start = link.find("<")
            end = link.find(">", start + 1)
            if start == -1 or end == -1:
                return None
            values = parse_qs(urlparse(link[start + 1 : end]).query).get("page")
            if values:
                return OrganizationAnalyzer._integer(values[0])
        return None

    @staticmethod
    def _normalize_login(login: str) -> str:
        """Validate and normalize an organization login."""

        normalized_login = login.strip()
        if not normalized_login:
            raise ValueError("organization login must not be empty")
        return normalized_login

    @staticmethod
    def _integer(value: object) -> int:
        """Convert GitHub count values safely."""

        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _optional_string(value: object) -> str | None:
        """Return a non-empty string value when available."""

        return value if isinstance(value, str) and value else None
