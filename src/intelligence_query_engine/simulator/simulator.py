"""Local, non-network simulation of Intelligence Query Engine preparation."""

from dataclasses import dataclass
from datetime import datetime, timezone

from intelligence_query_engine.ai.query_builder import _QUERY_CACHE
from intelligence_query_engine.common.cache import CacheStatistics
from intelligence_query_engine.common.query_pipeline import ProcessedQueryPlan
from intelligence_query_engine.common.query_validator import ValidationResult
from intelligence_query_engine.iqe import IQE


@dataclass(frozen=True)
class SimulationStatistics:
    """Aggregate statistics for one simulated intelligence plan."""

    category_count: int
    total_queries: int
    average_queries_per_category: float


@dataclass(frozen=True)
class SimulationReport:
    """Typed result of a local IQE preparation simulation."""

    generated_categories: list[str]
    total_queries: int
    validation_result: ValidationResult
    quality_metrics: dict[str, float | int]
    cache_statistics: CacheStatistics | None
    execution_summary: str
    estimated_execution_cost: float
    generated_timestamp: datetime
    statistics: SimulationStatistics


class IQESimulator:
    """Simulate the local preparation phase of intelligence collection."""

    _ESTIMATED_COST_PER_QUERY = 0.0001

    def __init__(self, iqe: IQE) -> None:
        """Initialize the simulator with the public IQE interface."""

        self._iqe = iqe

    def simulate(
        self,
        project_name: str,
        ecosystem: str | None = None,
        category: str | None = None,
    ) -> SimulationReport:
        """Prepare an IQE plan locally and return its simulated execution report."""

        processed_plan = self._iqe.build(
            project_name=project_name,
            ecosystem=ecosystem,
            category=category,
        )
        return self._build_report(processed_plan)

    def _build_report(self, processed_plan: ProcessedQueryPlan) -> SimulationReport:
        """Convert a processed plan into a concise, non-network report."""

        generated_categories = list(processed_plan.processed_queries)
        total_queries = processed_plan.quality_metrics["total_queries"]
        category_count = len(generated_categories)
        average_queries = (
            total_queries / category_count
            if category_count
            else 0.0
        )

        return SimulationReport(
            generated_categories=generated_categories,
            total_queries=total_queries,
            validation_result=processed_plan.validation_result,
            quality_metrics=dict(processed_plan.quality_metrics),
            cache_statistics=_QUERY_CACHE.statistics(),
            execution_summary=(
                "Prepared a local intelligence collection plan without "
                "contacting external services."
            ),
            estimated_execution_cost=round(
                total_queries * self._ESTIMATED_COST_PER_QUERY,
                4,
            ),
            generated_timestamp=datetime.now(timezone.utc),
            statistics=SimulationStatistics(
                category_count=category_count,
                total_queries=total_queries,
                average_queries_per_category=round(average_queries, 2),
            ),
        )
