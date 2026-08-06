"""GitHub contributor metadata collection and repository health intelligence."""

import json
import math
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from .client import GitHubClient
from .models import Contributor


@dataclass(frozen=True)
class ContributorIntelligence:
    """Normalized contributor profile and repository-level intelligence signals."""

    username: str
    display_name: str | None
    github_id: int
    account_type: str
    profile_url: str | None
    avatar_url: str | None
    bio: str | None
    company: str | None
    location: str | None
    blog: str | None
    email: str | None
    twitter_username: str | None
    hireable: bool | None
    followers: int
    following: int
    public_repositories: int
    public_gists: int
    created_at: str | None
    updated_at: str | None
    contribution_count: int
    contribution_percentage: float
    organization_memberships: tuple[str, ...]
    is_core_maintainer: bool
    bus_factor_contributor: bool
    single_maintainer_risk: bool
    is_bot: bool
    contributor_diversity_score: float
    maintainer_activity_score: float
    top_contributor_dependency: float
    repository_bus_factor: int


class ContributorAnalyzer:
    """Collect contributor profiles and compute repository sustainability signals."""

    def __init__(
        self,
        client: GitHubClient | None = None,
        opener: Callable[..., Any] | None = None,
    ) -> None:
        """Initialize with reusable GitHub HTTP dependencies."""

        self.client = client or GitHubClient()
        self._opener = opener or urlopen

    def analyze(self, owner: str, repository: str) -> list[ContributorIntelligence]:
        """Collect and analyze all public contributors for one repository."""

        normalized_owner = self._path_part(owner, "repository owner")
        normalized_repository = self._path_part(repository, "repository name")
        contributors = self._fetch_contributors(normalized_owner, normalized_repository)
        profiles: dict[str, Mapping[str, Any]] = {}
        organizations: dict[str, Iterable[object]] = {}
        for contributor in contributors:
            profiles[contributor.login] = self._fetch_mapping(
                self.client.prepare_request(f"/users/{contributor.login}")
            )
            organizations[contributor.login] = self._fetch_organizations(
                contributor.login
            )
        return self.analyze_contributors(contributors, profiles, organizations)

    def analyze_contributors(
        self,
        contributors: Iterable[Contributor],
        profiles: Mapping[str, Mapping[str, Any]] | None = None,
        organizations: Mapping[str, Iterable[object]] | None = None,
    ) -> list[ContributorIntelligence]:
        """Analyze supplied GitHub models and API payloads without network access."""

        contributor_list = list(contributors)
        profile_map = profiles or {}
        organization_map = organizations or {}
        total_contributions = sum(max(0, item.contributions) for item in contributor_list)
        percentages = [
            self.contribution_percentage(item.contributions, total_contributions)
            for item in contributor_list
        ]
        bus_factor = self.calculate_bus_factor(contributor_list)
        bus_factor_logins = self._bus_factor_logins(contributor_list)
        diversity_score = self.calculate_diversity_score(contributor_list)
        top_dependency = round(sum(sorted(percentages, reverse=True)[:3]), 2)
        human_contributors = sum(
            not self.detect_bot(item.login, profile_map.get(item.login))
            for item in contributor_list
        )
        single_maintainer_risk = (
            bool(contributor_list)
            and bus_factor == 1
            and (human_contributors <= 1 or max(percentages, default=0.0) >= 50.0)
        )

        intelligence: list[ContributorIntelligence] = []
        for contributor, percentage in zip(contributor_list, percentages):
            profile = profile_map.get(contributor.login, {})
            is_bot = self.detect_bot(contributor.login, profile)
            intelligence.append(
                ContributorIntelligence(
                    username=str(profile.get("login") or contributor.login),
                    display_name=self._optional_string(profile.get("name")),
                    github_id=self._integer(profile.get("id", contributor.id)),
                    account_type=str(profile.get("type") or ("Bot" if is_bot else "User")),
                    profile_url=self._optional_string(
                        profile.get("html_url", contributor.html_url)
                    ),
                    avatar_url=self._optional_string(
                        profile.get("avatar_url", contributor.avatar_url)
                    ),
                    bio=self._optional_string(profile.get("bio")),
                    company=self._optional_string(profile.get("company")),
                    location=self._optional_string(profile.get("location")),
                    blog=self._optional_string(profile.get("blog")),
                    email=self._optional_string(profile.get("email")),
                    twitter_username=self._optional_string(
                        profile.get("twitter_username")
                    ),
                    hireable=self._optional_bool(profile.get("hireable")),
                    followers=self._integer(profile.get("followers")),
                    following=self._integer(profile.get("following")),
                    public_repositories=self._integer(profile.get("public_repos")),
                    public_gists=self._integer(profile.get("public_gists")),
                    created_at=self._optional_string(profile.get("created_at")),
                    updated_at=self._optional_string(profile.get("updated_at")),
                    contribution_count=max(0, contributor.contributions),
                    contribution_percentage=percentage,
                    organization_memberships=self._organization_names(
                        organization_map.get(contributor.login, [])
                    ),
                    is_core_maintainer=(
                        not is_bot
                        and (percentage >= 10.0 or contributor.login in bus_factor_logins)
                    ),
                    bus_factor_contributor=contributor.login in bus_factor_logins,
                    single_maintainer_risk=single_maintainer_risk,
                    is_bot=is_bot,
                    contributor_diversity_score=diversity_score,
                    maintainer_activity_score=self._activity_score(
                        profile.get("updated_at"), percentage, is_bot
                    ),
                    top_contributor_dependency=top_dependency,
                    repository_bus_factor=bus_factor,
                )
            )
        return intelligence

    @staticmethod
    def contribution_percentage(contributions: int, total: int) -> float:
        """Return a contributor's percentage of repository contributions."""

        if total <= 0:
            return 0.0
        return round(max(0, contributions) / total * 100.0, 2)

    @staticmethod
    def detect_bot(
        username: str, profile: Mapping[str, Any] | None = None
    ) -> bool:
        """Detect GitHub bots using account type and established login patterns."""

        account_type = str((profile or {}).get("type", "")).casefold()
        normalized = username.casefold()
        return account_type == "bot" or normalized.endswith("[bot]") or any(
            marker in normalized
            for marker in ("dependabot", "renovate-bot", "github-actions")
        )

    @staticmethod
    def calculate_diversity_score(contributors: Iterable[Contributor]) -> float:
        """Calculate normalized Shannon diversity from contribution distribution."""

        counts = [max(0, item.contributions) for item in contributors]
        positive_counts = [count for count in counts if count > 0]
        total = sum(positive_counts)
        if total == 0 or len(positive_counts) <= 1:
            return 0.0
        entropy = -sum(
            (count / total) * math.log(count / total) for count in positive_counts
        )
        return round(entropy / math.log(len(positive_counts)) * 100.0, 2)

    @staticmethod
    def calculate_bus_factor(contributors: Iterable[Contributor]) -> int:
        """Return the fewest top contributors responsible for at least 50 percent."""

        counts = sorted(
            (max(0, item.contributions) for item in contributors), reverse=True
        )
        total = sum(counts)
        if total == 0:
            return 0
        cumulative = 0
        for index, count in enumerate(counts, start=1):
            cumulative += count
            if cumulative * 2 >= total:
                return index
        return len(counts)

    def _fetch_contributors(self, owner: str, repository: str) -> list[Contributor]:
        """Fetch all pages of public repository contributors."""

        request: Request | None = self.client.prepare_request(
            f"/repos/{owner}/{repository}/contributors?per_page=100"
        )
        contributors: list[Contributor] = []
        while request is not None:
            payload, headers = self._fetch(request)
            if not isinstance(payload, list):
                break
            contributors.extend(self.parse_contributors(payload))
            next_url = self._linked_url(headers.get("Link", ""), "next")
            request = self.client.prepare_request(next_url) if next_url else None
        return contributors

    @staticmethod
    def parse_contributors(payload: Iterable[object]) -> list[Contributor]:
        """Convert GitHub contributor payloads to existing contributor models."""

        return [
            Contributor(
                login=str(item.get("login") or ""),
                id=ContributorAnalyzer._integer(item.get("id")),
                contributions=ContributorAnalyzer._integer(item.get("contributions")),
                avatar_url=ContributorAnalyzer._optional_string(item.get("avatar_url")),
                html_url=ContributorAnalyzer._optional_string(item.get("html_url")),
            )
            for item in payload
            if isinstance(item, Mapping) and item.get("login")
        ]

    def _fetch_organizations(self, username: str) -> Iterable[object]:
        """Fetch public organization memberships when GitHub exposes them."""

        try:
            payload, _ = self._fetch(
                self.client.prepare_request(f"/users/{username}/orgs?per_page=100")
            )
        except HTTPError as error:
            if error.code in {403, 404}:
                return []
            raise
        return payload if isinstance(payload, list) else []

    def _fetch_mapping(self, request: Request) -> Mapping[str, Any]:
        payload, _ = self._fetch(request)
        return payload if isinstance(payload, Mapping) else {}

    def _fetch(self, request: Request) -> tuple[Any, Mapping[str, str]]:
        self.client.rate_limiter.ensure_available()
        with self._opener(request, timeout=self.client.config.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            headers = response.headers
        self._update_rate_limit(headers)
        return payload, headers

    def _update_rate_limit(self, headers: Mapping[str, str]) -> None:
        remaining = headers.get("X-RateLimit-Remaining")
        used = headers.get("X-RateLimit-Used")
        reset = headers.get("X-RateLimit-Reset")
        if remaining is not None and used is not None and reset is not None:
            self.client.rate_limiter.update(
                self._integer(remaining), self._integer(used), self._integer(reset)
            )

    @staticmethod
    def _bus_factor_logins(contributors: list[Contributor]) -> set[str]:
        total = sum(max(0, item.contributions) for item in contributors)
        if total == 0:
            return set()
        cumulative = 0
        logins: set[str] = set()
        for contributor in sorted(
            contributors, key=lambda item: item.contributions, reverse=True
        ):
            cumulative += max(0, contributor.contributions)
            logins.add(contributor.login)
            if cumulative * 2 >= total:
                break
        return logins

    @staticmethod
    def _activity_score(updated_at: object, percentage: float, is_bot: bool) -> float:
        if is_bot:
            return 0.0
        recency_score = 0.0
        if isinstance(updated_at, str):
            try:
                updated = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
                if updated.tzinfo is None:
                    updated = updated.replace(tzinfo=timezone.utc)
                age = max(0, (datetime.now(timezone.utc) - updated).days)
                recency_score = 60.0 if age <= 30 else 45.0 if age <= 90 else 30.0 if age <= 180 else 15.0 if age <= 365 else 0.0
            except ValueError:
                pass
        return round(min(100.0, recency_score + min(40.0, percentage)), 2)

    @staticmethod
    def _organization_names(values: Iterable[object]) -> tuple[str, ...]:
        names: list[str] = []
        for value in values:
            name = value.get("login") if isinstance(value, Mapping) else value
            if name and str(name) not in names:
                names.append(str(name))
        return tuple(names)

    @staticmethod
    def _linked_url(link_header: str, relation: str) -> str | None:
        for link in link_header.split(","):
            if f'rel="{relation}"' not in link:
                continue
            start, end = link.find("<"), link.find(">")
            return link[start + 1 : end] if start >= 0 and end > start else None
        return None

    @staticmethod
    def _path_part(value: str, label: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"{label} must not be empty")
        if "/" in normalized:
            raise ValueError(f"{label} must be a single path component")
        return normalized

    @staticmethod
    def _integer(value: object) -> int:
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _optional_string(value: object) -> str | None:
        return value if isinstance(value, str) and value else None

    @staticmethod
    def _optional_bool(value: object) -> bool | None:
        return value if isinstance(value, bool) else None
