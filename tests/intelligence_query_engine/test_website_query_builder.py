"""Tests for website discovery queries."""

from intelligence_query_engine.website.query_builder import WebsiteQueryBuilder


def test_website_builder_returns_expected_categories(project_name: str) -> None:
    queries = WebsiteQueryBuilder(project_name).build()

    assert "official_websites" in queries
    assert "documentation" in queries
    assert queries["documentation"][:3] == [
        "Monad docs",
        "Monad documentation",
        "Monad developer docs",
    ]
    assert all(isinstance(query, str) for values in queries.values() for query in values)
