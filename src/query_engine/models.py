from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Protocol

class QueryError(Exception): pass
class QueryValidationError(QueryError): pass
class QueryExecutionError(QueryError): pass
class PredicateOperator(StrEnum): EQ="eq"; NE="ne"; GT="gt"; GTE="gte"; LT="lt"; LTE="lte"; IN="in"; CONTAINS="contains"
class SortDirection(StrEnum): ASC="asc"; DESC="desc"
class AggregationType(StrEnum): COUNT="count"; SUM="sum"; AVERAGE="average"; MINIMUM="minimum"; MAXIMUM="maximum"; DISTINCT="distinct"
@dataclass(frozen=True, slots=True)
class Predicate: field: str; operator: PredicateOperator; value: Any
@dataclass(frozen=True, slots=True)
class Filter: predicates: tuple[Predicate, ...] = ()
@dataclass(frozen=True, slots=True)
class Projection: fields: tuple[str, ...] = ()
@dataclass(frozen=True, slots=True)
class Aggregation: operation: AggregationType; field: str | None = None; group_by: str | None = None
@dataclass(frozen=True, slots=True)
class Sorting: field: str; direction: SortDirection = SortDirection.ASC
@dataclass(frozen=True, slots=True)
class Pagination: limit: int = 100; offset: int = 0
@dataclass(frozen=True, slots=True)
class Ranking: field: str = "confidence"; descending: bool = True
@dataclass(frozen=True, slots=True)
class RelationshipTraversal: source_id: str; relationship: str; max_depth: int = 1
@dataclass(frozen=True, slots=True)
class QueryContext: execution_id: str; trace_id: str | None = None; metadata: tuple[tuple[str, str], ...] = ()
@dataclass(frozen=True, slots=True)
class Query:
    query_id: str; domain: str; filters: tuple[Filter, ...] = (); projection: Projection = Projection(); aggregations: tuple[Aggregation, ...] = (); sorting: tuple[Sorting, ...] = (); ranking: Ranking | None = None; pagination: Pagination = Pagination(); relationships: tuple[RelationshipTraversal, ...] = (); time_range: tuple[datetime | None, datetime | None] | None = None; metadata: tuple[tuple[str, str], ...] = ()
@dataclass(frozen=True, slots=True)
class QueryPlan: query: Query; ordered_predicates: tuple[Predicate, ...]; projected_fields: tuple[str, ...]; traversals: tuple[RelationshipTraversal, ...]
@dataclass(frozen=True, slots=True)
class QueryStatistics: scanned: int; matched: int; returned: int; duration_ms: float; cache_hit: bool = False
@dataclass(frozen=True, slots=True)
class QueryResult: query_id: str; items: tuple[Any, ...]; aggregations: tuple[tuple[str, Any], ...] = (); statistics: QueryStatistics | None = None
@dataclass(frozen=True, slots=True)
class QueryExecution: plan: QueryPlan; context: QueryContext; result: QueryResult
@dataclass(frozen=True, slots=True)
class CacheEntry: query_hash: str; result: QueryResult; expires_at: datetime; metadata: tuple[tuple[str, str], ...] = ()
class QueryStrategy(Protocol):
    def execute(self, plan: QueryPlan, values: tuple[Any, ...], context: QueryContext) -> QueryResult: ...
class QueryCache(Protocol):
    def get(self, query_hash: str, now: datetime | None = None) -> CacheEntry | None: ...
    def put(self, entry: CacheEntry) -> None: ...

class ImmutableQueryCache:
    def __init__(self): self._entries: dict[str, CacheEntry] = {}
    def get(self, query_hash: str, now: datetime | None = None) -> CacheEntry | None:
        entry=self._entries.get(query_hash); current=now or datetime.now(UTC)
        return entry if entry and entry.expires_at > current else None
    def put(self, entry: CacheEntry) -> None: self._entries[entry.query_hash]=entry

class QueryRegistry:
    def __init__(self): self._queries: dict[str, Query] = {}
    def register(self, query: Query) -> None: self._queries[query.query_id]=query
    def get(self, query_id: str) -> Query | None: return self._queries.get(query_id)
