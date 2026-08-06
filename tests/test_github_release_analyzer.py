"""Focused tests for GitHub release intelligence."""

from datetime import datetime, timedelta, timezone

from src.github_intelligence import ReleaseAnalyzer
from src.github_intelligence.models import Release


NOW = datetime(2026, 8, 6, 12, 0, tzinfo=timezone.utc)


def release(
    days_ago: int,
    tag: str,
    prerelease: bool = False,
    draft: bool = False,
) -> Release:
    return Release(
        id=days_ago,
        tag_name=tag,
        name=tag,
        prerelease=prerelease,
        draft=draft,
        published_at=(NOW - timedelta(days=days_ago)).isoformat(),
        author_login="maintainer",
    )


def test_semantic_version_parsing() -> None:
    assert ReleaseAnalyzer.parse_semantic_version("v2.4.1") == (2, 4, 1, None)
    assert ReleaseAnalyzer.parse_semantic_version("1.0.0-rc.1") == (1, 0, 0, "rc.1")
    assert ReleaseAnalyzer.parse_semantic_version("1.2") is None
    assert ReleaseAnalyzer.parse_semantic_version("01.2.3") is None


def test_cadence_calculation_uses_release_history() -> None:
    releases = [release(90, "v1.0.0"), release(60, "v1.1.0"), release(30, "v1.2.0")]

    intelligence = ReleaseAnalyzer().analyze_releases(releases, now=NOW)

    assert intelligence.release_frequency > 12.0
    assert intelligence.release_cadence == "frequent"
    assert intelligence.average_days_between_releases == 30.0


def test_maturity_scoring_rewards_stable_history_and_major_versions() -> None:
    mature = ReleaseAnalyzer.maturity_score(12, 12, 730, 2)
    early = ReleaseAnalyzer.maturity_score(2, 1, 30, 0)

    assert mature == 100.0
    assert mature > early


def test_release_interval_calculation() -> None:
    timestamps = [NOW - timedelta(days=90), NOW - timedelta(days=60), NOW - timedelta(days=10)]

    intervals = ReleaseAnalyzer.release_intervals(timestamps)
    intelligence = ReleaseAnalyzer().analyze_releases(
        [release(90, "v1.0.0"), release(60, "v1.1.0"), release(10, "v1.2.0")],
        now=NOW,
    )

    assert intervals == [30.0, 50.0]
    assert intelligence.median_release_interval == 40.0
    assert intelligence.longest_release_gap == 50.0
    assert intelligence.shortest_release_gap == 30.0


def test_stability_scoring_penalizes_prereleases_and_drafts() -> None:
    stable_score = ReleaseAnalyzer.stability_score(5, 5, 0, 0)
    unstable_score = ReleaseAnalyzer.stability_score(5, 1, 3, 1)

    assert stable_score == 100.0
    assert unstable_score < stable_score

    intelligence = ReleaseAnalyzer().analyze_releases(
        [
            release(40, "v1.0.0"),
            release(30, "v1.1.0-rc.1", prerelease=True),
            release(20, "candidate", prerelease=True),
            release(10, "nightly", prerelease=True),
        ],
        now=NOW,
    )
    assert intelligence.excessive_prereleases is True
    assert intelligence.unstable_versioning is True
