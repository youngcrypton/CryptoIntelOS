"""GitHub release, tag, cadence, maturity, and maintenance intelligence."""

import json
import re
import statistics
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.request import Request, urlopen

from .client import GitHubClient
from .commit_analyzer import CommitIntelligence
from .contributor_analyzer import ContributorIntelligence
from .models import Release


@dataclass(frozen=True)
class ReleaseIntelligence:
    """Normalized release history, delivery signals, scores, and risks."""

    total_releases: int
    latest_release: str | None
    latest_release_date: str | None
    first_release_date: str | None
    release_frequency: float
    average_days_between_releases: float | None
    release_tags: tuple[str, ...]
    prerelease_count: int
    stable_release_count: int
    draft_release_count: int
    semantic_version_usage: float
    latest_version: str | None
    release_authors: tuple[str, ...]
    semantic_version_compliance: bool
    release_cadence: str
    release_consistency: str
    release_maturity: str
    release_stability: str
    maintenance_quality: str
    release_adoption_readiness: bool
    days_since_latest_release: int | None
    median_release_interval: float | None
    longest_release_gap: float | None
    shortest_release_gap: float | None
    release_health_score: float
    release_consistency_score: float
    maintenance_score: float
    project_maturity_score: float
    version_quality_score: float
    stability_score: float
    abandoned_releases: bool
    never_released_repository: bool
    excessive_prereleases: bool
    irregular_release_schedule: bool
    stalled_maintenance: bool
    outdated_releases: bool
    unstable_versioning: bool


class ReleaseAnalyzer:
    """Collect GitHub releases and tags and derive software-delivery intelligence."""

    _SEMVER_PATTERN = re.compile(
        r"^[vV]?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
        r"(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
        r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
    )

    def __init__(
        self,
        client: GitHubClient | None = None,
        opener: Callable[..., Any] | None = None,
    ) -> None:
        """Initialize with reusable GitHub HTTP dependencies."""

        self.client = client or GitHubClient()
        self._opener = opener or urlopen

    def analyze(
        self,
        owner: str,
        repository: str,
        commits: CommitIntelligence | None = None,
        contributors: Iterable[ContributorIntelligence] | None = None,
    ) -> ReleaseIntelligence:
        """Collect all available releases and tags for one repository."""

        owner_part = self._path_part(owner, "repository owner")
        repository_part = self._path_part(repository, "repository name")
        releases = self._fetch_releases(owner_part, repository_part)
        tags = self._fetch_tags(owner_part, repository_part)
        return self.analyze_releases(releases, tags, commits, contributors)

    def analyze_releases(
        self,
        releases: Iterable[Release],
        tags: Iterable[str] | None = None,
        commits: CommitIntelligence | None = None,
        contributors: Iterable[ContributorIntelligence] | None = None,
        now: datetime | None = None,
    ) -> ReleaseIntelligence:
        """Analyze supplied release models without performing network requests."""

        reference_time = self._as_utc(now or datetime.now(timezone.utc))
        release_list = list(releases)
        dated_releases = sorted(
            (
                (timestamp, release)
                for release in release_list
                if (timestamp := self._parse_timestamp(release.published_at)) is not None
            ),
            key=lambda item: item[0],
        )
        timestamps = [item[0] for item in dated_releases]
        first = timestamps[0] if timestamps else None
        latest = timestamps[-1] if timestamps else None
        latest_release_model = dated_releases[-1][1] if dated_releases else None
        intervals = self.release_intervals(timestamps)
        total = len(release_list)
        stable_count = sum(
            not release.prerelease and not release.draft for release in release_list
        )
        prerelease_count = sum(release.prerelease for release in release_list)
        draft_count = sum(release.draft for release in release_list)
        release_tag_values = self._unique_tags(
            [release.tag_name for release in release_list], tags or []
        )
        parsed_versions = [
            parsed
            for release in release_list
            if (parsed := self.parse_semantic_version(release.tag_name)) is not None
        ]
        semantic_usage = round(len(parsed_versions) / total * 100.0, 2) if total else 0.0
        latest_version = (
            latest_release_model.tag_name
            if latest_release_model
            and self.parse_semantic_version(latest_release_model.tag_name)
            else None
        )
        days_since_latest = (
            max(0, (reference_time - latest).days) if latest else None
        )
        history_days = max(1, (latest - first).days) if first and latest else 1
        release_frequency = round(total / history_days * 365.25, 4) if total else 0.0
        consistency_score = self.consistency_score(intervals)
        stability_score = self.stability_score(total, stable_count, prerelease_count, draft_count)
        latest_major = (
            self.parse_semantic_version(latest_version)[0] if latest_version else 0
        )
        maturity_score = self.maturity_score(
            total, stable_count, history_days, latest_major
        )
        version_score = self._version_quality_score(
            semantic_usage, latest_version, release_tag_values
        )
        maintenance_score = self._maintenance_score(
            days_since_latest, consistency_score, commits, contributors
        )
        health_score = round(
            0.25 * consistency_score
            + 0.2 * stability_score
            + 0.2 * maintenance_score
            + 0.2 * maturity_score
            + 0.15 * version_score,
            2,
        )
        excessive_prereleases = (
            prerelease_count >= 3 and prerelease_count / max(total, 1) > 0.5
        )
        never_released = total == 0
        abandoned = days_since_latest is not None and days_since_latest >= 365
        outdated = days_since_latest is not None and days_since_latest >= 180
        stalled = bool(
            commits
            and commits.active_development
            and (days_since_latest is None or days_since_latest >= 180)
        )
        unstable_versioning = total > 0 and (
            semantic_usage < 50.0 or excessive_prereleases
        )
        irregular = len(intervals) >= 2 and consistency_score < 40.0
        cadence = self._cadence(release_frequency, days_since_latest)
        stability = self._quality_label(stability_score)
        maintenance = self._quality_label(maintenance_score)
        maturity = self._maturity_label(maturity_score)
        adoption_ready = (
            health_score >= 70.0
            and stable_count > 0
            and not outdated
            and not unstable_versioning
        )

        return ReleaseIntelligence(
            total_releases=total,
            latest_release=(
                latest_release_model.name or latest_release_model.tag_name
                if latest_release_model
                else None
            ),
            latest_release_date=latest.isoformat() if latest else None,
            first_release_date=first.isoformat() if first else None,
            release_frequency=release_frequency,
            average_days_between_releases=(
                round(statistics.mean(intervals), 4) if intervals else None
            ),
            release_tags=release_tag_values,
            prerelease_count=prerelease_count,
            stable_release_count=stable_count,
            draft_release_count=draft_count,
            semantic_version_usage=semantic_usage,
            latest_version=latest_version,
            release_authors=tuple(
                dict.fromkeys(
                    release.author_login
                    for release in release_list
                    if release.author_login
                )
            ),
            semantic_version_compliance=total > 0 and semantic_usage == 100.0,
            release_cadence=cadence,
            release_consistency=self._quality_label(consistency_score),
            release_maturity=maturity,
            release_stability=stability,
            maintenance_quality=maintenance,
            release_adoption_readiness=adoption_ready,
            days_since_latest_release=days_since_latest,
            median_release_interval=(
                round(statistics.median(intervals), 4) if intervals else None
            ),
            longest_release_gap=round(max(intervals), 4) if intervals else None,
            shortest_release_gap=round(min(intervals), 4) if intervals else None,
            release_health_score=health_score,
            release_consistency_score=consistency_score,
            maintenance_score=maintenance_score,
            project_maturity_score=maturity_score,
            version_quality_score=version_score,
            stability_score=stability_score,
            abandoned_releases=abandoned,
            never_released_repository=never_released,
            excessive_prereleases=excessive_prereleases,
            irregular_release_schedule=irregular,
            stalled_maintenance=stalled,
            outdated_releases=outdated,
            unstable_versioning=unstable_versioning,
        )

    @classmethod
    def parse_semantic_version(
        cls, value: str | None
    ) -> tuple[int, int, int, str | None] | None:
        """Parse a strict Semantic Version tag, allowing a conventional v prefix."""

        if not value:
            return None
        match = cls._SEMVER_PATTERN.fullmatch(value.strip())
        if not match:
            return None
        return (
            int(match.group(1)),
            int(match.group(2)),
            int(match.group(3)),
            match.group(4),
        )

    @staticmethod
    def release_intervals(timestamps: Iterable[datetime]) -> list[float]:
        """Return chronological intervals between releases measured in days."""

        ordered = sorted(ReleaseAnalyzer._as_utc(value) for value in timestamps)
        return [
            (current - previous).total_seconds() / 86400
            for previous, current in zip(ordered, ordered[1:])
        ]

    @staticmethod
    def consistency_score(intervals: Iterable[float]) -> float:
        """Score cadence consistency using interval coefficient of variation."""

        values = list(intervals)
        if not values:
            return 0.0
        if len(values) == 1:
            return 70.0
        mean = statistics.mean(values)
        if mean <= 0:
            return 0.0
        coefficient = statistics.pstdev(values) / mean
        return round(max(0.0, min(100.0, (1.0 - coefficient) * 100.0)), 2)

    @staticmethod
    def maturity_score(
        total_releases: int,
        stable_releases: int,
        history_days: int,
        latest_major_version: int,
    ) -> float:
        """Score release maturity from history, volume, stability, and major version."""

        if total_releases <= 0:
            return 0.0
        history_score = min(25.0, max(0, history_days) / 730 * 25.0)
        volume_score = min(25.0, total_releases / 10 * 25.0)
        stable_score = min(30.0, stable_releases / total_releases * 30.0)
        version_score = min(20.0, max(0, latest_major_version) * 10.0)
        return round(history_score + volume_score + stable_score + version_score, 2)

    @staticmethod
    def stability_score(
        total_releases: int,
        stable_releases: int,
        prereleases: int,
        drafts: int,
    ) -> float:
        """Score the proportion of consumable stable releases."""

        if total_releases <= 0:
            return 0.0
        stable_ratio = stable_releases / total_releases
        prerelease_ratio = prereleases / total_releases
        draft_ratio = drafts / total_releases
        return round(
            max(0.0, min(100.0, stable_ratio * 100 - prerelease_ratio * 20 - draft_ratio * 10)),
            2,
        )

    def _fetch_releases(self, owner: str, repository: str) -> list[Release]:
        payloads = self._fetch_paginated(
            f"/repos/{owner}/{repository}/releases?per_page=100"
        )
        return self.parse_releases(payloads)

    def _fetch_tags(self, owner: str, repository: str) -> list[str]:
        payloads = self._fetch_paginated(
            f"/repos/{owner}/{repository}/tags?per_page=100"
        )
        return [
            str(item.get("name"))
            for item in payloads
            if isinstance(item, Mapping) and item.get("name")
        ]

    def _fetch_paginated(self, path: str) -> list[object]:
        request: Request | None = self.client.prepare_request(path)
        items: list[object] = []
        while request is not None:
            payload, headers = self._fetch(request)
            if not isinstance(payload, list):
                break
            items.extend(payload)
            next_url = self._linked_url(headers.get("Link", ""), "next")
            request = self.client.prepare_request(next_url) if next_url else None
        return items

    @staticmethod
    def parse_releases(payload: Iterable[object]) -> list[Release]:
        """Convert GitHub release API payloads into existing release models."""

        releases: list[Release] = []
        for item in payload:
            if not isinstance(item, Mapping) or not item.get("tag_name"):
                continue
            author = item.get("author")
            author_mapping = author if isinstance(author, Mapping) else {}
            releases.append(
                Release(
                    id=ReleaseAnalyzer._integer(item.get("id")),
                    tag_name=str(item.get("tag_name")),
                    name=ReleaseAnalyzer._optional_string(item.get("name")),
                    body=ReleaseAnalyzer._optional_string(item.get("body")),
                    prerelease=bool(item.get("prerelease", False)),
                    draft=bool(item.get("draft", False)),
                    published_at=ReleaseAnalyzer._optional_string(
                        item.get("published_at")
                    ),
                    html_url=ReleaseAnalyzer._optional_string(item.get("html_url")),
                    author_login=ReleaseAnalyzer._optional_string(
                        author_mapping.get("login")
                    ),
                )
            )
        return releases

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
    def _version_quality_score(
        semantic_usage: float, latest_version: str | None, tags: tuple[str, ...]
    ) -> float:
        score = semantic_usage * 0.8
        if latest_version:
            score += 15.0
        if len(tags) == len(set(tags)):
            score += 5.0
        return round(min(100.0, score), 2)

    @staticmethod
    def _maintenance_score(
        days_since_latest: int | None,
        consistency_score: float,
        commits: CommitIntelligence | None,
        contributors: Iterable[ContributorIntelligence] | None,
    ) -> float:
        freshness = 0.0
        if days_since_latest is not None:
            freshness = max(0.0, 100.0 - days_since_latest / 365 * 100.0)
        commit_score = commits.commit_health_score if commits else consistency_score
        contributor_list = list(contributors or [])
        maintainer_score = (
            statistics.mean(
                contributor.maintainer_activity_score
                for contributor in contributor_list
                if contributor.is_core_maintainer and not contributor.is_bot
            )
            if any(
                contributor.is_core_maintainer and not contributor.is_bot
                for contributor in contributor_list
            )
            else consistency_score
        )
        return round(
            min(100.0, 0.4 * freshness + 0.35 * commit_score + 0.25 * maintainer_score),
            2,
        )

    @staticmethod
    def _cadence(frequency: float, days_since_latest: int | None) -> str:
        if days_since_latest is None:
            return "none"
        if days_since_latest >= 365:
            return "abandoned"
        if frequency >= 12:
            return "frequent"
        if frequency >= 4:
            return "regular"
        if frequency >= 1:
            return "infrequent"
        return "sporadic"

    @staticmethod
    def _quality_label(score: float) -> str:
        if score >= 80:
            return "high"
        if score >= 60:
            return "moderate"
        if score >= 40:
            return "low"
        return "poor"

    @staticmethod
    def _maturity_label(score: float) -> str:
        if score >= 80:
            return "mature"
        if score >= 60:
            return "established"
        if score >= 35:
            return "developing"
        return "early"

    @staticmethod
    def _unique_tags(primary: Iterable[str], secondary: Iterable[str]) -> tuple[str, ...]:
        return tuple(dict.fromkeys([*primary, *secondary]))

    @staticmethod
    def _parse_timestamp(value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return ReleaseAnalyzer._as_utc(
                datetime.fromisoformat(value.replace("Z", "+00:00"))
            )
        except ValueError:
            return None

    @staticmethod
    def _as_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

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
