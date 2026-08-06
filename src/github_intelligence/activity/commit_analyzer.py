"""Commit activity metric analysis."""

from collections import Counter
from collections.abc import Iterable
from datetime import datetime, timezone

from ..models import Commit


class CommitAnalyzer:
    """Analyze commit frequency, velocity, contributors, and trends."""

    def analyze(self, commits: Iterable[Commit]) -> dict[str, object]:
        """Return deterministic commit metrics from supplied commit models."""

        commit_list = list(commits)
        timestamps = sorted(
            timestamp
            for commit in commit_list
            if (timestamp := self._parse_timestamp(commit.authored_at)) is not None
        )
        contributor_activity = dict(
            Counter(
                commit.author_login or commit.author_name or "unknown"
                for commit in commit_list
            )
        )
        velocity = self._velocity(timestamps)
        trend = self._trend(timestamps)
        return {
            "commit_count": len(commit_list),
            "commit_frequency": len(commit_list),
            "commit_velocity_per_day": velocity,
            "contributor_activity": contributor_activity,
            "last_commit_timestamp": (
                timestamps[-1].isoformat() if timestamps else None
            ),
            "development_trend_indicators": trend,
        }

    @staticmethod
    def _velocity(timestamps: list[datetime]) -> float:
        """Return commits per elapsed day between the first and last commit."""

        if len(timestamps) < 2:
            return float(len(timestamps))
        elapsed_days = max((timestamps[-1] - timestamps[0]).total_seconds() / 86400, 1)
        return round((len(timestamps) - 1) / elapsed_days, 4)

    @staticmethod
    def _trend(timestamps: list[datetime]) -> list[str]:
        """Return simple development trend indicators."""

        if not timestamps:
            return ["no_timestamped_commits"]
        if len(timestamps) < 2:
            return ["insufficient_history"]
        intervals = [
            (current - previous).total_seconds()
            for previous, current in zip(timestamps, timestamps[1:])
        ]
        average_interval = sum(intervals) / len(intervals)
        return [
            "steady_activity" if average_interval <= 30 * 86400 else "sporadic_activity",
            "recent_activity" if (datetime.now(timezone.utc) - timestamps[-1]).days <= 90 else "stale_activity",
        ]

    @staticmethod
    def _parse_timestamp(value: str | None) -> datetime | None:
        """Parse a GitHub ISO timestamp as UTC."""

        if not value:
            return None
        try:
            timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return timestamp.replace(tzinfo=timezone.utc) if timestamp.tzinfo is None else timestamp
