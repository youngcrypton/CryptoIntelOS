"""Focused tests for GitHub contributor intelligence."""

from src.github_intelligence import ContributorAnalyzer
from src.github_intelligence.models import Contributor


def contributor(login: str, contributions: int, github_id: int = 1) -> Contributor:
    return Contributor(login=login, id=github_id, contributions=contributions)


def test_parse_contributors_uses_existing_model() -> None:
    parsed = ContributorAnalyzer.parse_contributors(
        [{"login": "alice", "id": 42, "contributions": 15, "html_url": "url"}]
    )

    assert parsed == [Contributor(login="alice", id=42, contributions=15, html_url="url")]


def test_bot_detection_uses_type_and_login_patterns() -> None:
    assert ContributorAnalyzer.detect_bot("release-helper", {"type": "Bot"})
    assert ContributorAnalyzer.detect_bot("dependabot[bot]")
    assert ContributorAnalyzer.detect_bot("renovate-bot")
    assert not ContributorAnalyzer.detect_bot("alice")


def test_diversity_scoring_rewards_balanced_contributions() -> None:
    balanced = [contributor("alice", 50), contributor("bob", 50)]
    concentrated = [contributor("alice", 99), contributor("bob", 1)]

    assert ContributorAnalyzer.calculate_diversity_score(balanced) == 100.0
    assert ContributorAnalyzer.calculate_diversity_score(concentrated) < 10.0


def test_bus_factor_is_minimum_group_reaching_half_of_contributions() -> None:
    contributors = [
        contributor("alice", 40),
        contributor("bob", 30),
        contributor("carol", 20),
        contributor("dave", 10),
    ]

    assert ContributorAnalyzer.calculate_bus_factor(contributors) == 2


def test_contribution_percentage_and_repository_signals() -> None:
    contributors = [contributor("alice", 75), contributor("bob", 25, 2)]
    profiles = {
        "alice": {"name": "Alice", "type": "User", "public_repos": 12},
        "bob": {"name": "Bob", "type": "User"},
    }

    intelligence = ContributorAnalyzer().analyze_contributors(
        contributors, profiles, {"alice": [{"login": "crypto-org"}]}
    )

    assert ContributorAnalyzer.contribution_percentage(25, 100) == 25.0
    assert intelligence[0].contribution_percentage == 75.0
    assert intelligence[0].organization_memberships == ("crypto-org",)
    assert intelligence[0].is_core_maintainer is True
    assert intelligence[0].bus_factor_contributor is True
    assert intelligence[0].single_maintainer_risk is True
    assert intelligence[0].top_contributor_dependency == 100.0
    assert intelligence[0].repository_bus_factor == 1
