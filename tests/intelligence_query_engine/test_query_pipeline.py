"""Tests for query-plan processing."""

from intelligence_query_engine.common.query_pipeline import QueryProcessingPipeline


def test_pipeline_normalizes_and_deduplicates_queries() -> None:
    result = QueryProcessingPipeline().process(
        {"docs": [" Monad   docs ", "Monad docs", "", "Monad API docs"]}
    )

    assert result.processed_queries == {"docs": ["Monad docs", "Monad API docs"]}
    assert result.validation_result.valid
    assert result.optimization_statistics["whitespace_normalizations"] == 1
    assert result.optimization_statistics["empty_queries_removed"] == 1
    assert result.optimization_statistics["duplicate_queries_removed"] == 1
    assert result.quality_metrics["total_queries"] == 2
