from dataclasses import dataclass
from typing import Any
from .models import Query, QueryResult, QueryStatistics
@dataclass(frozen=True, slots=True)
class QueryRequest: query: Query; values: tuple[Any,...] = ()
@dataclass(frozen=True, slots=True)
class QueryResponse: result: QueryResult
@dataclass(frozen=True, slots=True)
class SearchRequest: text: str; domain: str; limit: int = 20
@dataclass(frozen=True, slots=True)
class SearchResponse: items: tuple[Any,...]
@dataclass(frozen=True, slots=True)
class QueryStatisticsResponse: statistics: QueryStatistics
QUERY_API_ROUTES=(('POST','/query'),('POST','/search'),('GET','/query/{id}'),('GET','/query/statistics'))
