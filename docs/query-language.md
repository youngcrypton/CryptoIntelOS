# Query Language

Queries may be constructed with `QueryBuilder` or JSON. A JSON query contains `query_id`, `domain`, `filters`, `projection`, `limit`, and `offset`. Filter operators are `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, and `contains`. Field paths use dots for nested attributes. Aggregations support count, sum, average, minimum, maximum, and distinct. Sorting and ranking are stable and deterministic.

Example: `{"query_id":"active","domain":"project","filters":[{"field":"confidence","operator":"gte","value":0.8}],"projection":["canonical_project_identifier","confidence"]}`.
