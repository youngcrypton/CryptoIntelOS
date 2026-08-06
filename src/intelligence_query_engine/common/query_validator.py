"""Validation utilities for intelligence query-builder output."""

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ValidationResult:
    """Structured result returned by :class:`QueryValidator`."""

    valid: bool
    duplicate_count: int
    empty_categories: list[str]
    invalid_queries: list[str]
    statistics: dict[str, int]


class QueryValidator:
    """Validate categorized query plans produced by intelligence builders."""

    def __init__(self, query_plan: object) -> None:
        """Initialize the validator with a builder's output."""

        self.query_plan = query_plan

    def validate_categories(self) -> list[str]:
        """Return category-level validation issues."""

        if not isinstance(self.query_plan, Mapping):
            return ["query plan must be a mapping of categories to query lists"]

        if not self.query_plan:
            return ["query plan must contain at least one category"]

        return [
            f"{category}: category name must be a non-empty string"
            for category in self.query_plan
            if not isinstance(category, str) or not category.strip()
        ]

    def validate_duplicates(self) -> int:
        """Return the total number of duplicate queries across all categories."""

        if not isinstance(self.query_plan, Mapping):
            return 0

        seen_queries: set[str] = set()
        duplicate_count = 0
        for queries in self.query_plan.values():
            if not isinstance(queries, list):
                continue

            for query in queries:
                if isinstance(query, str) and query in seen_queries:
                    duplicate_count += 1
                elif isinstance(query, str):
                    seen_queries.add(query)

        return duplicate_count

    def validate_empty_queries(self) -> list[str]:
        """Return locations of empty or whitespace-only query strings."""

        if not isinstance(self.query_plan, Mapping):
            return []

        return [
            f"{category}[{index}]: empty query"
            for category, queries in self.query_plan.items()
            if isinstance(queries, list)
            for index, query in enumerate(queries)
            if isinstance(query, str) and not query.strip()
        ]

    def validate_query_types(self) -> list[str]:
        """Return locations whose containers or values have invalid types."""

        if not isinstance(self.query_plan, Mapping):
            return []

        invalid_queries: list[str] = []
        for category, queries in self.query_plan.items():
            if not isinstance(queries, list):
                invalid_queries.append(
                    f"{category}: queries must be a list"
                )
                continue

            invalid_queries.extend(
                f"{category}[{index}]: query must be a string"
                for index, query in enumerate(queries)
                if not isinstance(query, str)
            )

        return invalid_queries

    def validate(self) -> ValidationResult:
        """Return a complete validation report for the supplied query plan."""

        category_issues = self.validate_categories()
        type_issues = self.validate_query_types()
        empty_query_issues = self.validate_empty_queries()
        empty_categories = self._find_empty_categories()
        duplicate_count = self.validate_duplicates()

        return ValidationResult(
            valid=not (
                category_issues
                or type_issues
                or empty_query_issues
                or empty_categories
                or duplicate_count
            ),
            duplicate_count=duplicate_count,
            empty_categories=empty_categories,
            invalid_queries=category_issues + type_issues + empty_query_issues,
            statistics=self._statistics(),
        )

    def _find_empty_categories(self) -> list[str]:
        """Return categories with valid list containers but no queries."""

        if not isinstance(self.query_plan, Mapping):
            return []

        return [
            category
            for category, queries in self.query_plan.items()
            if isinstance(category, str) and isinstance(queries, list) and not queries
        ]

    def _statistics(self) -> dict[str, int]:
        """Return summary counts for the supplied query plan."""

        if not isinstance(self.query_plan, Mapping):
            return {
                "category_count": 0,
                "query_count": 0,
                "string_query_count": 0,
            }

        query_lists = [
            queries
            for queries in self.query_plan.values()
            if isinstance(queries, list)
        ]
        return {
            "category_count": len(self.query_plan),
            "query_count": sum(len(queries) for queries in query_lists),
            "string_query_count": sum(
                isinstance(query, str)
                for queries in query_lists
                for query in queries
            ),
        }
