"""End-to-end tests for the public IQE facade."""

from intelligence_query_engine import IQE
from intelligence_query_engine.common.query_pipeline import ProcessedQueryPlan


def test_iqe_builds_processed_plan(project_name: str) -> None:
    result = IQE().build(project_name, ecosystem="Ethereum", category="L2")

    assert isinstance(result, ProcessedQueryPlan)
    assert result.validation_result.valid
    assert result.quality_metrics["completeness_score"] == 100.0
    assert "google" in result.processed_queries
