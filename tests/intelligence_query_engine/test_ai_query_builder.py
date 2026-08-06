"""Tests for unified AI query-plan generation and caching."""

from intelligence_query_engine.ai.query_builder import AIQueryBuilder, _QUERY_CACHE


def test_ai_builder_returns_unified_contextual_plan(project_name: str) -> None:
    plan = AIQueryBuilder(project_name, ecosystem="Ethereum", category="L2").build()

    assert set(plan) == {
        "twitter", "websites", "google", "launchpads", "wallets", "funding",
        "partnerships", "governance", "documentation", "audits", "developers",
        "ecosystem",
    }
    assert "Monad official website Ethereum L2" in plan["websites"]


def test_ai_builder_reuses_cached_plan(project_name: str) -> None:
    _QUERY_CACHE.clear()

    first_plan = AIQueryBuilder(project_name).build()
    second_plan = AIQueryBuilder(project_name).build()
    statistics = _QUERY_CACHE.statistics()

    assert first_plan == second_plan
    assert statistics.cache_misses == 1
    assert statistics.cache_hits == 1
