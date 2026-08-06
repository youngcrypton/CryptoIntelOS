"""Focused tests for temporal GitHub commit intelligence."""

from datetime import datetime, timedelta, timezone

from src.github_intelligence import CommitAnalyzer
from src.github_intelligence.models import Commit


NOW = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)


def commit(days_ago: float, author: str = "alice", message: str = "change") -> Commit:
    authored_at = (NOW - timedelta(days=days_ago)).isoformat()
    return Commit(
        sha=f"{author}-{days_ago}-{message}",
        message=message,
        author_login=author,
        authored_at=authored_at,
    )


def test_velocity_calculation_rewards_recent_volume() -> None:
    assert CommitAnalyzer.velocity_score(20, 30) > CommitAnalyzer.velocity_score(5, 30)
    assert CommitAnalyzer.velocity_score(50, 60) == 100.0


def test_dormancy_and_abandonment_detection() -> None:
    dormant = CommitAnalyzer().analyze_commits([commit(120)], now=NOW)
    abandoned = CommitAnalyzer().analyze_commits([commit(400)], now=NOW)

    assert dormant.dormant_development is True
    assert dormant.abandoned_repository is False
    assert abandoned.abandoned_repository is True
    assert abandoned.abandoned_maintenance is True


def test_burst_detection_identifies_abnormal_daily_volume() -> None:
    commits = [commit(1, message=f"burst-{index}") for index in range(12)]
    commits.extend(commit(days) for days in (10, 20, 30, 40))

    intelligence = CommitAnalyzer().analyze_commits(commits, now=NOW)

    assert intelligence.burst_activity is True
    assert intelligence.fake_activity_spikes is True


def test_activity_trend_detects_acceleration_and_decline() -> None:
    accelerating = [commit(day) for day in (1, 2, 3, 4, 5, 35, 40)]
    declining = [commit(1), *[commit(day) for day in range(31, 41)]]

    accelerated = CommitAnalyzer().analyze_commits(accelerating, now=NOW)
    slowed = CommitAnalyzer().analyze_commits(declining, now=NOW)

    assert accelerated.accelerating_activity is True
    assert accelerated.recent_activity_trend == 150.0
    assert slowed.declining_activity is True
    assert slowed.recent_activity_trend == -90.0


def test_freshness_scoring_uses_days_since_latest_commit() -> None:
    assert CommitAnalyzer.freshness_score(0) == 100.0
    assert CommitAnalyzer.freshness_score(14) == 75.0
    assert CommitAnalyzer.freshness_score(400) == 0.0
    assert CommitAnalyzer.freshness_score(None) == 0.0


def test_commit_interval_calculations_use_days() -> None:
    commits = [commit(6), commit(4), commit(1)]

    intelligence = CommitAnalyzer().analyze_commits(commits, now=NOW)

    assert intelligence.median_commit_interval == 2.5
    assert intelligence.average_commit_interval == 2.5
    assert intelligence.longest_inactivity_period == 3.0
