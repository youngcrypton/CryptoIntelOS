"""Processing pipeline for intelligence query-builder output."""

from dataclasses import dataclass
from typing import Mapping

from intelligence_query_engine.common.query_validator import QueryValidator, ValidationResult


@dataclass(frozen=True)
class ProcessedQueryPlan:
    """Normalized, deduplicated query plan and its processing metadata."""

    processed_queries: dict[str, list[str]]
    validation_result: ValidationResult
    quality_metrics: dict[str, float | int]
    optimization_statistics: dict[str, int]


class QueryProcessingPipeline:
    """Validate, optimize, deduplicate, and score a categorized query plan."""

    def process(self, queries: object) -> ProcessedQueryPlan:
        """Return a normalized and quality-scored version of a builder's output."""

        QueryValidator(queries).validate()
        processed_queries, optimization_statistics = self._optimize(queries)
        validation_result = QueryValidator(processed_queries).validate()
        quality_metrics = self._quality_metrics(
            processed_queries,
            optimization_statistics,
        )
        return ProcessedQueryPlan(
            processed_queries=processed_queries,
            validation_result=validation_result,
            quality_metrics=quality_metrics,
            optimization_statistics=optimization_statistics,
        )

    def _optimize(self, queries: object) -> tuple[dict[str, list[str]], dict[str, int]]:
        """Normalize strings and remove empty, invalid, and duplicate queries."""

        processed_queries: dict[str, list[str]] = {}
        seen_queries: set[str] = set()
        statistics = {
            "whitespace_normalizations": 0,
            "empty_queries_removed": 0,
            "invalid_queries_removed": 0,
            "duplicate_queries_removed": 0,
        }

        if not isinstance(queries, Mapping):
            return processed_queries, statistics

        for category, category_queries in queries.items():
            if not isinstance(category, str) or not category.strip():
                continue

            processed_category = category.strip()
            processed_queries[processed_category] = []
            if not isinstance(category_queries, list):
                statistics["invalid_queries_removed"] += 1
                continue

            for query in category_queries:
                if not isinstance(query, str):
                    statistics["invalid_queries_removed"] += 1
                    continue

                normalized_query = " ".join(query.split())
                if normalized_query != query:
                    statistics["whitespace_normalizations"] += 1
                if not normalized_query:
                    statistics["empty_queries_removed"] += 1
                    continue
                if normalized_query in seen_queries:
                    statistics["duplicate_queries_removed"] += 1
                    continue

                seen_queries.add(normalized_query)
                processed_queries[processed_category].append(normalized_query)

        return processed_queries, statistics

    @staticmethod
    def _quality_metrics(
        processed_queries: dict[str, list[str]],
        optimization_statistics: dict[str, int],
    ) -> dict[str, float | int]:
        """Calculate lightweight completeness and coverage metrics."""

        category_count = len(processed_queries)
        total_queries = sum(
            len(category_queries)
            for category_queries in processed_queries.values()
        )
        covered_categories = sum(
            bool(category_queries)
            for category_queries in processed_queries.values()
        )
        category_coverage = (
            (covered_categories / category_count) * 100
            if category_count
            else 0.0
        )
        average_queries_per_category = (
            total_queries / category_count
            if category_count
            else 0.0
        )
        completeness_score = round(
            min(
                100.0,
                (category_coverage * 0.7)
                + (min(average_queries_per_category / 3, 1.0) * 30),
            ),
            2,
        )

        return {
            "total_queries": total_queries,
            "duplicate_removal_count": optimization_statistics[
                "duplicate_queries_removed"
            ],
            "category_coverage": round(category_coverage, 2),
            "average_queries_per_category": round(
                average_queries_per_category,
                2,
            ),
            "completeness_score": completeness_score,
        }
