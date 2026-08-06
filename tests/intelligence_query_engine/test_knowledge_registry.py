"""Tests for registered knowledge packs."""

from intelligence_query_engine.knowledge_registry import knowledge_registry


def test_knowledge_registry_returns_ecosystems_and_domains() -> None:
    registry = knowledge_registry.get_all()

    assert set(registry) == {"ecosystems", "domains"}
    assert registry["ecosystems"]
    assert registry["domains"]
    assert all(
        set(pack) == {"hashtags", "keywords", "boolean_queries"}
        for pack in registry["ecosystems"].values()
    )
