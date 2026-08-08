from __future__ import annotations
import hashlib, json, time
from dataclasses import asdict, is_dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from .models import *

def field_value(value: Any, path: str) -> Any:
    current=value
    for part in path.split("."):
        current=current.get(part) if isinstance(current, dict) else getattr(current, part, None)
    return current
def matches(value: Any, predicate: Predicate) -> bool:
    actual=field_value(value,predicate.field); expected=predicate.value; op=predicate.operator
    if op is PredicateOperator.EQ: return actual == expected
    if op is PredicateOperator.NE: return actual != expected
    if op is PredicateOperator.GT: return actual is not None and actual > expected
    if op is PredicateOperator.GTE: return actual is not None and actual >= expected
    if op is PredicateOperator.LT: return actual is not None and actual < expected
    if op is PredicateOperator.LTE: return actual is not None and actual <= expected
    if op is PredicateOperator.IN: return actual in expected
    if op is PredicateOperator.CONTAINS: return expected in actual if actual is not None else False
    return False
class QueryValidator:
    def validate(self, query: Query) -> Query:
        if not query.query_id or not query.domain: raise QueryValidationError("query_id and domain are required")
        if query.pagination.limit < 0 or query.pagination.offset < 0: raise QueryValidationError("pagination values must be non-negative")
        return query
class QueryOptimizer:
    def optimize(self, query: Query) -> QueryPlan:
        predicates=tuple(sorted((p for group in query.filters for p in group.predicates), key=lambda p:(p.operator not in {PredicateOperator.EQ, PredicateOperator.IN}, p.field)))
        return QueryPlan(query,predicates,query.projection.fields,tuple(sorted(query.relationships,key=lambda r:r.max_depth)))
class QueryBuilder:
    def __init__(self, query_id: str, domain: str): self.query_id=query_id; self.domain=domain; self.predicates=[]; self.fields=[]
    def where(self, field: str, operator: PredicateOperator, value: Any): self.predicates.append(Predicate(field,operator,value)); return self
    def select(self,*fields: str): self.fields.extend(fields); return self
    def build(self): return Query(self.query_id,self.domain,(Filter(tuple(self.predicates)),),Projection(tuple(self.fields)))
class QueryParser:
    def parse(self, value: str | dict[str,Any]) -> Query:
        data=json.loads(value) if isinstance(value,str) else value
        predicates=tuple(Predicate(p["field"],PredicateOperator(p.get("operator","eq")),p.get("value")) for p in data.get("filters",()))
        return Query(data.get("query_id","query"),data["domain"],(Filter(predicates),),Projection(tuple(data.get("projection",()))),pagination=Pagination(data.get("limit",100),data.get("offset",0)))
class RelationshipGraph:
    def __init__(self, edges: tuple[tuple[str,str,str],...]=()): self.edges=edges
    def traverse(self, request: RelationshipTraversal) -> tuple[str,...]:
        found=[]; frontier=[request.source_id]; seen={request.source_id}
        for _ in range(request.max_depth):
            next_frontier=[]
            for source,relation,target in self.edges:
                if source in frontier and relation==request.relationship and target not in seen: found.append(target); seen.add(target); next_frontier.append(target)
            frontier=next_frontier
        return tuple(found)
class QueryEngine:
    def __init__(self, cache: QueryCache | None=None, graph: RelationshipGraph | None=None): self.cache=cache or ImmutableQueryCache(); self.graph=graph or RelationshipGraph()
    def execute(self, query: Query, values: tuple[Any,...], context: QueryContext) -> QueryExecution:
        query=QueryValidator().validate(query); plan=QueryOptimizer().optimize(query); key=hashlib.sha256(repr(query).encode()).hexdigest(); cached=self.cache.get(key)
        if cached: return QueryExecution(plan,context,QueryResult(query.query_id,cached.result.items,cached.result.aggregations,QueryStatistics(0,len(cached.result.items),len(cached.result.items),0,True)))
        start=time.perf_counter(); filtered=tuple(v for v in values if all(matches(v,p) for p in plan.ordered_predicates)); scanned=len(values)
        if query.time_range:
            lower,upper=query.time_range
            filtered=tuple(v for v in filtered if (stamp:=next((field_value(v,name) for name in ("timestamp","generated_at","observed_at","collected_at") if field_value(v,name) is not None),None)) is not None and (lower is None or stamp>=lower) and (upper is None or stamp<=upper))
        for sort in reversed(query.sorting): filtered=tuple(sorted(filtered,key=lambda v:(field_value(v,sort.field) is None,field_value(v,sort.field)),reverse=sort.direction is SortDirection.DESC))
        if query.ranking: filtered=tuple(sorted(filtered,key=lambda v:field_value(v,query.ranking.field) or 0,reverse=query.ranking.descending))
        aggregations=[]
        for agg in query.aggregations:
            if agg.group_by:
                groups={}
                for item in filtered: groups.setdefault(field_value(item,agg.group_by),[]).append(item)
                aggregations.append((f"group:{agg.group_by}",tuple((key,len(items)) for key,items in sorted(groups.items(),key=lambda pair:str(pair[0])))))
                continue
            vals=[field_value(v,agg.field) for v in filtered] if agg.field else list(filtered); vals=[v for v in vals if v is not None]
            result={AggregationType.COUNT:lambda:len(vals),AggregationType.SUM:lambda:sum(vals),AggregationType.AVERAGE:lambda:sum(vals)/len(vals) if vals else 0,AggregationType.MINIMUM:lambda:min(vals) if vals else None,AggregationType.MAXIMUM:lambda:max(vals) if vals else None,AggregationType.DISTINCT:lambda:tuple(dict.fromkeys(vals))}[agg.operation]()
            aggregations.append((f"{agg.operation}:{agg.field or '*'}",result))
        for traversal in plan.traversals: aggregations.append((f"relationship:{traversal.relationship}",self.graph.traverse(traversal)))
        page=filtered[query.pagination.offset:query.pagination.offset+query.pagination.limit]
        if plan.projected_fields: page=tuple({f:field_value(v,f) for f in plan.projected_fields} for v in page)
        stats=QueryStatistics(scanned,len(filtered),len(page),(time.perf_counter()-start)*1000); result=QueryResult(query.query_id,page,tuple(aggregations),stats)
        self.cache.put(CacheEntry(key,result,datetime.now(UTC)+timedelta(minutes=5),context.metadata)); return QueryExecution(plan,context,result)
