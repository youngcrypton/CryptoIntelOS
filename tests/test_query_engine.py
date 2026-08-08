import json, time
from src.query_engine import *
from src.cli import main

VALUES=({"project":"alpha","confidence":.9,"score":90,"source":"github"},{"project":"beta","confidence":.6,"score":70,"source":"website"})
def test_parse_validate_filter_projection_sort_rank_paginate_and_cache():
    query=QueryParser().parse({"query_id":"q1","domain":"project","filters":[{"field":"confidence","operator":"gte","value":.7}],"projection":["project","score"],"limit":1})
    engine=QueryEngine(); first=engine.execute(query,VALUES,QueryContext("e1")); second=engine.execute(query,VALUES,QueryContext("e2"))
    assert first.result.items==({"project":"alpha","score":90},)
    assert second.result.statistics.cache_hit
def test_aggregation_sorting_ranking_and_graph():
    query=Query("q2","project",aggregations=(Aggregation(AggregationType.AVERAGE,"score"),),sorting=(Sorting("confidence",SortDirection.DESC),),ranking=Ranking("score"),pagination=Pagination(10,0))
    result=QueryEngine().execute(query,VALUES,QueryContext("e")).result
    assert result.aggregations[0][1]==80
    assert RelationshipGraph((("project:a","wallet","wallet:1"),)).traverse(RelationshipTraversal("project:a","wallet")) == ("wallet:1",)
def test_api_contracts_and_cli(capsys):
    assert ("POST","/query") in QUERY_API_ROUTES
    expression=json.dumps({"query_id":"cli","domain":"project","filters":[]})
    assert main(["query",expression,"--data",json.dumps(list(VALUES)),"--json"])==0
    assert "alpha" in capsys.readouterr().out
def test_query_benchmark_under_reasonable_fixture_budget():
    values=tuple({"project":str(i),"confidence":i/1000} for i in range(1000)); query=QueryBuilder("bench","project").where("confidence",PredicateOperator.GTE,.5).build(); start=time.perf_counter(); result=QueryEngine().execute(query,values,QueryContext("bench")); elapsed=(time.perf_counter()-start)*1000
    assert len(result.result.items)==100
    assert elapsed < 500
