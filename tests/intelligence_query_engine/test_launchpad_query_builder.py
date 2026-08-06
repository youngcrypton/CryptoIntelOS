"""Tests for launchpad discovery queries."""

from intelligence_query_engine.launchpads.query_builder import LaunchpadQueryBuilder


def test_launchpad_builder_returns_expected_categories(project_name: str) -> None:
    queries = LaunchpadQueryBuilder(project_name).build()

    assert set(queries) >= {"coinlist", "daomaker", "seedify", "ecosystem_launches"}
    assert queries["coinlist"][:2] == ["CoinList Monad", "Monad CoinList"]
    assert all(len(values) == 3 for values in queries.values())
