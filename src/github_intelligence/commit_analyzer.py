"""Temporal GitHub commit intelligence and repository maintenance signals."""

import json
import statistics
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.request import Request, urlopen

from .client import GitHubClient
from .contributor_analyzer import ContributorIntelligence
from .models import Commit


@dataclass(frozen=True)
class CommitIntelligence:
    """Commit-history metrics, activity signals, scores, and maintenance risks."""

    total_commit_count: int
    commits_last_24_hours: int
    commits_last_7_days: int
    commits_last_30_days: int
    commits_last_90_days: int
    commits_last_year: int
    average_commits_per_day: float
    average_commits_per_week: float
    average_commits_per_month: float
    first_commit_date: str | None
    latest_commit_date: str | None
    repository_age: int
    days_since_last_commit: int | None
    active_development: bool
    dormant_development: bool
    abandoned_repository: bool
    burst_activity: bool
    sustained_development: bool
    declining_activity: bool
    accelerating_activity: bool
    release_preparation_activity: bool
    weekday_commit_count: int
    weekend_commit_count: int
    hourly_activity_distribution: dict[int, int]
    maintainer_activity_concentration: float
    contributor_commit_distribution: dict[str, int]
    development_velocity_score: float
    repository_freshness_score: float
    development_consistency_score: float
    dormancy_risk_score: float
    commit_health_score: float
    contributor_activity_score: float
    commit_frequency: float
    median_commit_interval: float | None
    average_commit_interval: float | None
    longest_inactivity_period: float | None
    recent_activity_trend: float
    single_developer_dependency: bool
    sudden_development_stop: bool
    fake_activity_spikes: bool
    mass_generated_commits: bool
    long_dormant_periods: bool
    abandoned_maintenance: bool


class CommitAnalyzer:
    """Collect repository commits and derive deterministic temporal intelligence."""

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
        contributors: Iterable[ContributorIntelligence] | None = None,
    ) -> CommitIntelligence:
        """Collect all available commits and analyze repository activity."""

        owner_part = self._path_part(owner, "repository owner")
        repository_part = self._path_part(repository, "repository name")
        commits = self._fetch_commits(owner_part, repository_part)
        return self.analyze_commits(commits, contributors=contributors)

    def analyze_commits(
        self,
        commits: Iterable[Commit],
        contributors: Iterable[ContributorIntelligence] | None = None,
        now: datetime | None = None,
    ) -> CommitIntelligence:
        """Analyze supplied commit models without performing network requests."""

        reference_time = self._as_utc(now or datetime.now(timezone.utc))
        commit_list = list(commits)
        dated_commits = sorted(
            (
                (timestamp, commit)
                for commit in commit_list
                if (timestamp := self._parse_timestamp(commit.authored_at)) is not None
            ),
            key=lambda item: item[0],
        )
        timestamps = [item[0] for item in dated_commits]
        contributor_distribution = dict(
            Counter(self._author(commit) for commit in commit_list)
        )
        total_count = len(commit_list)
        first = timestamps[0] if timestamps else None
        latest = timestamps[-1] if timestamps else None
        repository_age = max(0, (reference_time - first).days) if first else 0
        days_since_last = max(0, (reference_time - latest).days) if latest else None
        intervals = self.commit_intervals(timestamps)
        window_counts = {
            days: self._count_since(timestamps, reference_time - timedelta(days=days))
            for days in (1, 7, 30, 90, 365)
        }
        daily_counts = Counter(timestamp.date() for timestamp in timestamps)
        trend = self.activity_trend(timestamps, reference_time)
        burst = self.detect_burst(daily_counts)
        sustained = self._sustained(timestamps, reference_time)
        declining = trend <= -25.0
        accelerating = trend >= 25.0
        active = window_counts[30] > 0 and days_since_last is not None and days_since_last <= 30
        dormant = days_since_last is not None and 90 <= days_since_last < 365
        abandoned = days_since_last is None or days_since_last >= 365
        sudden_stop = self._sudden_stop(timestamps, reference_time)
        concentration = self._maintainer_concentration(
            contributor_distribution, contributors
        )
        single_dependency = (
            bool(contributor_distribution) and concentration >= 75.0
        )
        freshness_score = self.freshness_score(days_since_last)
        velocity_score = self.velocity_score(window_counts[30], window_counts[90])
        consistency_score = self._consistency_score(daily_counts, first, latest)
        contributor_score = self._contributor_score(contributor_distribution)
        dormancy_score = self._dormancy_score(days_since_last, sudden_stop)
        commit_health_score = round(
            max(
                0.0,
                min(
                    100.0,
                    0.25 * velocity_score
                    + 0.25 * freshness_score
                    + 0.2 * consistency_score
                    + 0.2 * contributor_score
                    + 0.1 * (100.0 - dormancy_score),
                ),
            ),
            2,
        )
        longest_interval = max(intervals, default=None)
        fake_spikes = self._fake_spikes(daily_counts, total_count, burst)
        mass_generated = self._mass_generated(commit_list)

        elapsed_days = max(repository_age, 1)
        average_per_day = round(total_count / elapsed_days, 4)
        return CommitIntelligence(
            total_commit_count=total_count,
            commits_last_24_hours=window_counts[1],
            commits_last_7_days=window_counts[7],
            commits_last_30_days=window_counts[30],
            commits_last_90_days=window_counts[90],
            commits_last_year=window_counts[365],
            average_commits_per_day=average_per_day,
            average_commits_per_week=round(average_per_day * 7, 4),
            average_commits_per_month=round(average_per_day * 30, 4),
            first_commit_date=first.isoformat() if first else None,
            latest_commit_date=latest.isoformat() if latest else None,
            repository_age=repository_age,
            days_since_last_commit=days_since_last,
            active_development=active,
            dormant_development=dormant,
            abandoned_repository=abandoned,
            burst_activity=burst,
            sustained_development=sustained,
            declining_activity=declining,
            accelerating_activity=accelerating,
            release_preparation_activity=self._release_preparation(
                dated_commits, reference_time
            ),
            weekday_commit_count=sum(timestamp.weekday() < 5 for timestamp in timestamps),
            weekend_commit_count=sum(timestamp.weekday() >= 5 for timestamp in timestamps),
            hourly_activity_distribution={
                hour: sum(timestamp.hour == hour for timestamp in timestamps)
                for hour in range(24)
            },
            maintainer_activity_concentration=concentration,
            contributor_commit_distribution=contributor_distribution,
            development_velocity_score=velocity_score,
            repository_freshness_score=freshness_score,
            development_consistency_score=consistency_score,
            dormancy_risk_score=dormancy_score,
            commit_health_score=commit_health_score,
            contributor_activity_score=contributor_score,
            commit_frequency=average_per_day,
            median_commit_interval=(
                round(statistics.median(intervals), 4) if intervals else None
            ),
            average_commit_interval=(
                round(statistics.mean(intervals), 4) if intervals else None
            ),
            longest_inactivity_period=(
                round(longest_interval, 4) if longest_interval is not None else None
            ),
            recent_activity_trend=trend,
            single_developer_dependency=single_dependency,
            sudden_development_stop=sudden_stop,
            fake_activity_spikes=fake_spikes,
            mass_generated_commits=mass_generated,
            long_dormant_periods=(
                longest_interval is not None and longest_interval >= 180.0
            ),
            abandoned_maintenance=abandoned and total_count > 0,
        )

    @staticmethod
    def velocity_score(commits_last_30_days: int, commits_last_90_days: int) -> float:
        """Score recent commit velocity, rewarding both volume and acceleration."""

        monthly_baseline = commits_last_90_days / 3
        volume_score = min(80.0, commits_last_30_days * 4.0)
        acceleration_bonus = (
            min(20.0, max(0.0, (commits_last_30_days - monthly_baseline) * 2.0))
            if monthly_baseline > 0
            else 0.0
        )
        return round(min(100.0, volume_score + acceleration_bonus), 2)

    @staticmethod
    def freshness_score(days_since_last_commit: int | None) -> float:
        """Score repository freshness from the age of its latest commit."""

        if days_since_last_commit is None:
            return 0.0
        if days_since_last_commit <= 1:
            return 100.0
        if days_since_last_commit <= 7:
            return 90.0
        if days_since_last_commit <= 30:
            return 75.0
        if days_since_last_commit <= 90:
            return 50.0
        if days_since_last_commit <= 180:
            return 25.0
        if days_since_last_commit <= 365:
            return 10.0
        return 0.0

    @staticmethod
    def commit_intervals(timestamps: Iterable[datetime]) -> list[float]:
        """Return chronological commit intervals measured in days."""

        ordered = sorted(CommitAnalyzer._as_utc(value) for value in timestamps)
        return [
            (current - previous).total_seconds() / 86400
            for previous, current in zip(ordered, ordered[1:])
        ]

    @staticmethod
    def activity_trend(timestamps: Iterable[datetime], now: datetime) -> float:
        """Compare the latest 30 days with the preceding 30-day period."""

        reference = CommitAnalyzer._as_utc(now)
        values = [CommitAnalyzer._as_utc(value) for value in timestamps]
        recent = sum(reference - timedelta(days=30) <= value <= reference for value in values)
        previous = sum(
            reference - timedelta(days=60) <= value < reference - timedelta(days=30)
            for value in values
        )
        if previous == 0:
            return 100.0 if recent > 0 else 0.0
        return round((recent - previous) / previous * 100.0, 2)

    @staticmethod
    def detect_burst(daily_counts: Mapping[object, int]) -> bool:
        """Detect a daily commit volume far above normal active-day activity."""

        counts = list(daily_counts.values())
        if not counts:
            return False
        median = statistics.median(counts)
        return max(counts) >= 10 and max(counts) >= max(3 * median, median + 5)

    def _fetch_commits(self, owner: str, repository: str) -> list[Commit]:
        request: Request | None = self.client.prepare_request(
            f"/repos/{owner}/{repository}/commits?per_page=100"
        )
        commits: list[Commit] = []
        while request is not None:
            payload, headers = self._fetch(request)
            if not isinstance(payload, list):
                break
            commits.extend(self.parse_commits(payload))
            next_url = self._linked_url(headers.get("Link", ""), "next")
            request = self.client.prepare_request(next_url) if next_url else None
        return commits

    @staticmethod
    def parse_commits(payload: Iterable[object]) -> list[Commit]:
        """Convert GitHub commit API payloads into existing commit models."""

        commits: list[Commit] = []
        for item in payload:
            if not isinstance(item, Mapping):
                continue
            commit_data = item.get("commit")
            commit_mapping = commit_data if isinstance(commit_data, Mapping) else {}
            author_data = item.get("author")
            author_mapping = author_data if isinstance(author_data, Mapping) else {}
            git_author = commit_mapping.get("author")
            git_author_mapping = git_author if isinstance(git_author, Mapping) else {}
            sha = item.get("sha")
            if not sha:
                continue
            commits.append(
                Commit(
                    sha=str(sha),
                    message=str(commit_mapping.get("message") or ""),
                    author_login=CommitAnalyzer._optional_string(
                        author_mapping.get("login")
                    ),
                    author_name=CommitAnalyzer._optional_string(
                        git_author_mapping.get("name")
                    ),
                    authored_at=CommitAnalyzer._optional_string(
                        git_author_mapping.get("date")
                    ),
                    html_url=CommitAnalyzer._optional_string(item.get("html_url")),
                )
            )
        return commits

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
    def _count_since(timestamps: Iterable[datetime], start: datetime) -> int:
        return sum(timestamp >= start for timestamp in timestamps)

    @staticmethod
    def _sustained(timestamps: list[datetime], now: datetime) -> bool:
        buckets = [
            sum(
                now - timedelta(days=30 * (index + 1)) <= timestamp < now - timedelta(days=30 * index)
                for timestamp in timestamps
            )
            for index in range(4)
        ]
        return sum(count > 0 for count in buckets) >= 3 and sum(buckets) >= 12

    @staticmethod
    def _sudden_stop(timestamps: list[datetime], now: datetime) -> bool:
        recent = sum(timestamp >= now - timedelta(days=30) for timestamp in timestamps)
        prior = sum(
            now - timedelta(days=120) <= timestamp < now - timedelta(days=30)
            for timestamp in timestamps
        )
        return recent == 0 and prior >= 12

    @staticmethod
    def _release_preparation(
        dated_commits: list[tuple[datetime, Commit]], now: datetime
    ) -> bool:
        keywords = ("release", "version", "changelog", "bump", "rc", "tag")
        recent_messages = [
            commit.message.casefold()
            for timestamp, commit in dated_commits
            if timestamp >= now - timedelta(days=30)
        ]
        return sum(any(keyword in message for keyword in keywords) for message in recent_messages) >= 2

    @staticmethod
    def _maintainer_concentration(
        distribution: Mapping[str, int],
        contributors: Iterable[ContributorIntelligence] | None,
    ) -> float:
        total = sum(distribution.values())
        if total == 0:
            return 0.0
        contributor_list = list(contributors or [])
        maintainer_names = {
            contributor.username
            for contributor in contributor_list
            if contributor.is_core_maintainer and not contributor.is_bot
        }
        if maintainer_names:
            maintainer_commits = sum(distribution.get(name, 0) for name in maintainer_names)
            return round(maintainer_commits / total * 100.0, 2)
        return round(max(distribution.values()) / total * 100.0, 2)

    @staticmethod
    def _consistency_score(
        daily_counts: Mapping[object, int],
        first: datetime | None,
        latest: datetime | None,
    ) -> float:
        if not first or not latest:
            return 0.0
        weeks = max(1, (latest - first).days // 7 + 1)
        active_weeks = len({date.isocalendar()[:2] for date in daily_counts})
        return round(min(100.0, active_weeks / weeks * 100.0), 2)

    @staticmethod
    def _contributor_score(distribution: Mapping[str, int]) -> float:
        total = sum(distribution.values())
        if total == 0:
            return 0.0
        shares = [count / total for count in distribution.values()]
        diversity = 1.0 - sum(share * share for share in shares)
        breadth = min(1.0, len(distribution) / 5)
        return round((0.7 * diversity + 0.3 * breadth) * 100.0, 2)

    @staticmethod
    def _dormancy_score(days_since_last: int | None, sudden_stop: bool) -> float:
        if days_since_last is None:
            return 100.0
        age_risk = min(100.0, days_since_last / 365 * 100.0)
        return round(min(100.0, age_risk + (25.0 if sudden_stop else 0.0)), 2)

    @staticmethod
    def _fake_spikes(
        daily_counts: Mapping[object, int], total: int, burst: bool
    ) -> bool:
        return bool(
            burst and total and max(daily_counts.values(), default=0) / total >= 0.6
        )

    @staticmethod
    def _mass_generated(commits: list[Commit]) -> bool:
        messages = [commit.message.strip().casefold() for commit in commits if commit.message.strip()]
        if len(messages) < 10:
            return False
        most_common = Counter(messages).most_common(1)[0][1]
        return most_common >= 10 and most_common / len(messages) >= 0.2

    @staticmethod
    def _author(commit: Commit) -> str:
        return commit.author_login or commit.author_name or "unknown"

    @staticmethod
    def _parse_timestamp(value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            return CommitAnalyzer._as_utc(
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
