"""Unified intelligence search-plan builder."""

import json
from typing import Final

from intelligence_query_engine.common.cache import QueryCache
from intelligence_query_engine.google.query_builder import GoogleDorkBuilder
from intelligence_query_engine.launchpads.query_builder import LaunchpadQueryBuilder
from intelligence_query_engine.wallets.query_builder import WalletQueryBuilder
from intelligence_query_engine.website.query_builder import WebsiteQueryBuilder


_QUERY_CACHE = QueryCache()


class AIQueryBuilder:
    """Orchestrate project discovery queries across intelligence sources."""

    _PLACEHOLDER_SUFFIXES: Final[dict[str, tuple[str, ...]]] = {
        "twitter": (
            "X Twitter",
            "announcement Twitter",
            "official account",
        ),
        "funding": (
            "funding round",
            "venture capital investors",
            "ecosystem fund",
        ),
        "partnerships": (
            "partnership",
            "integration",
            "strategic alliance",
        ),
        "governance": (
            "governance",
            "DAO proposal",
            "governance forum",
        ),
        "audits": (
            "audit report",
            "smart contract audit",
            "security review",
        ),
        "developers": (
            "developer SDK",
            "developer tools",
            "developer grant",
        ),
        "ecosystem": (
            "ecosystem",
            "ecosystem expansion",
            "developer ecosystem",
        ),
    }

    def __init__(
        self,
        project_name: str,
        ecosystem: str | None = None,
        category: str | None = None,
    ) -> None:
        """Initialize the builder with project and optional query context."""

        self.project_name = self._normalize_required(project_name, "project_name")
        self.ecosystem = self._normalize_optional(ecosystem)
        self.category = self._normalize_optional(category)

    def build(self) -> dict[str, list[str]]:
        """Return a unified, categorized intelligence search plan."""

        cache_key = self._cache_key()
        cached_plan = _QUERY_CACHE.get(cache_key)
        if cached_plan is not None:
            return cached_plan

        website_queries = WebsiteQueryBuilder(self.project_name).build()
        google_queries = GoogleDorkBuilder(self.project_name).build()

        plan = {
            "twitter": self._placeholder_queries("twitter"),
            "websites": website_queries["official_websites"],
            "google": self._flatten_queries(google_queries),
            "launchpads": self._flatten_queries(
                LaunchpadQueryBuilder(self.project_name).build()
            ),
            "wallets": self._flatten_queries(
                WalletQueryBuilder(self.project_name).build()
            ),
            "funding": self._placeholder_queries("funding"),
            "partnerships": self._placeholder_queries("partnerships"),
            "governance": self._placeholder_queries("governance"),
            "documentation": website_queries["documentation"],
            "audits": self._placeholder_queries("audits"),
            "developers": self._placeholder_queries("developers"),
            "ecosystem": self._placeholder_queries("ecosystem"),
        }
        query_plan = {
            query_category: self._with_context(queries)
            for query_category, queries in plan.items()
        }
        _QUERY_CACHE.set(cache_key, query_plan)
        return query_plan

    def _placeholder_queries(self, query_category: str) -> list[str]:
        """Build source-shaped queries for categories without a dedicated builder."""

        return [
            f"{self.project_name} {suffix}"
            for suffix in self._PLACEHOLDER_SUFFIXES[query_category]
        ]

    def _cache_key(self) -> str:
        """Build a stable cache key for this builder request."""

        return json.dumps(
            {
                "builder_type": type(self).__name__,
                "project_name": self.project_name,
                "ecosystem": self.ecosystem,
                "category": self.category,
            },
            sort_keys=True,
            separators=(",", ":"),
        )

    def _with_context(self, queries: list[str]) -> list[str]:
        """Append optional ecosystem and category context to each query."""

        if not self._context:
            return queries

        return [f"{query} {self._context}" for query in queries]

    @staticmethod
    def _flatten_queries(grouped_queries: dict[str, list[str]]) -> list[str]:
        """Flatten a builder's grouped output while preserving query order."""

        return [
            query
            for queries in grouped_queries.values()
            for query in queries
        ]

    @property
    def _context(self) -> str:
        """Return optional ecosystem and category terms as one suffix."""

        return " ".join(
            term
            for term in (self.ecosystem, self.category)
            if term is not None
        )

    @staticmethod
    def _normalize_required(value: str, parameter_name: str) -> str:
        """Normalize a required non-empty string parameter."""

        normalized_value = value.strip()
        if not normalized_value:
            raise ValueError(f"{parameter_name} must not be empty")
        return normalized_value

    @staticmethod
    def _normalize_optional(value: str | None) -> str | None:
        """Normalize an optional string, treating blank input as absent."""

        if value is None:
            return None

        normalized_value = value.strip()
        return normalized_value or None
