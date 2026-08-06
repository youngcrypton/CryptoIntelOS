"""Unified public interface for the Intelligence Query Engine."""

from intelligence_query_engine.ai.query_builder import AIQueryBuilder
from intelligence_query_engine.common.query_pipeline import ProcessedQueryPlan, QueryProcessingPipeline


class IQE:
    """Build validated, optimized intelligence search plans through one API."""

    def __init__(self) -> None:
        """Initialize the reusable processing pipeline."""

        self._pipeline = QueryProcessingPipeline()

    def build(
        self,
        project_name: str,
        ecosystem: str | None = None,
        category: str | None = None,
    ) -> ProcessedQueryPlan:
        """Build and process a unified intelligence plan for a project."""

        generated_queries = AIQueryBuilder(
            project_name=project_name,
            ecosystem=ecosystem,
            category=category,
        ).build()
        return self._pipeline.process(generated_queries)
