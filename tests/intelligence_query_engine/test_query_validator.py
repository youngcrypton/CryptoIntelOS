"""Tests for structured query-plan validation."""

from intelligence_query_engine.common.query_validator import QueryValidator


def test_query_validator_accepts_valid_plan() -> None:
    result = QueryValidator({"docs": ["Monad docs", "Monad API docs"]}).validate()

    assert result.valid
    assert result.duplicate_count == 0
    assert result.empty_categories == []
    assert result.invalid_queries == []


def test_query_validator_reports_invalid_values() -> None:
    result = QueryValidator({"docs": ["Monad docs", "", "Monad docs", 1], "empty": []}).validate()

    assert not result.valid
    assert result.duplicate_count == 1
    assert result.empty_categories == ["empty"]
    assert result.invalid_queries
