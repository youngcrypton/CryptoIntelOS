"""Tests for Google dork query generation."""

from intelligence_query_engine.google.query_builder import GoogleDorkBuilder


def test_google_dork_builder_returns_operator_queries(project_name: str) -> None:
    queries = GoogleDorkBuilder(project_name).build()

    assert set(queries) >= {"official", "github", "whitepaper", "news"}
    assert 'site:github.com "Monad"' in queries["github"]
    assert 'filetype:pdf "Monad" whitepaper' in queries["whitepaper"]
    assert all(len(values) == len(set(values)) for values in queries.values())
