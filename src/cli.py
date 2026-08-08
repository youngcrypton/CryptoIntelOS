"""Production CLI for deterministic provider-to-profile validation."""
from __future__ import annotations
import argparse, json
from io import StringIO
from datetime import UTC, datetime
from src.core_intelligence.identity import Entity, EntityType, Identifier, IdentifierType, Identity
from src.unified_intelligence.entity_linking import EntityCandidate
from src.unified_intelligence.profile import SourceIntelligence, UnifiedIntelligenceVerticalSlice
from src.query_engine import QueryContext, QueryEngine, QueryParser, QueryOptimizer

def _source(kind: str, identifier: str) -> SourceIntelligence:
    identifier_type = {"github": IdentifierType.GITHUB_REPOSITORY_ID, "website": IdentifierType.URL, "wallet": IdentifierType.WALLET_ADDRESS, "project": IdentifierType.EXTERNAL_ID}[kind]
    candidate = EntityCandidate(kind, Entity(entity_type=EntityType.PROJECT, identity=Identity(canonical_name=identifier, identifiers=(Identifier(identifier, identifier_type),))), identifier, (Identifier(identifier, identifier_type),))
    return SourceIntelligence(kind, candidate)

def main(argv: list[str] | None = None) -> int:
    parser=argparse.ArgumentParser(prog="cryptointel"); sub=parser.add_subparsers(dest="command", required=True)
    for name in ("github", "website", "wallet", "project"):
        command=sub.add_parser(name); command.add_argument("identifier"); command.add_argument("--json", action="store_true"); command.add_argument("--pretty", action="store_true"); command.add_argument("--trace", action="store_true"); command.add_argument("--debug", action="store_true"); command.add_argument("--provider")
    for name in ("query", "search", "explain-query"):
        command=sub.add_parser(name); command.add_argument("expression"); command.add_argument("--data", default="[]"); command.add_argument("--json", action="store_true"); command.add_argument("--pretty", action="store_true"); command.add_argument("--trace", action="store_true"); command.add_argument("--statistics", action="store_true")
    args=parser.parse_args(argv)
    if args.command in {"query", "search", "explain-query"}:
        if args.command == "search":
            values=tuple(json.loads(args.data)); term=args.expression.casefold(); items=tuple(value for value in values if term in json.dumps(value,default=str).casefold())
            print(json.dumps({"items":items,"statistics":{"matched":len(items)}},indent=2 if args.pretty else None,default=str)); return 0
        query=QueryParser().parse(args.expression)
        if args.command == "explain-query":
            output={"plan": repr(QueryOptimizer().optimize(query))}
        else:
            execution=QueryEngine().execute(query,tuple(json.loads(args.data)),QueryContext(f"cli:{query.query_id}"))
            output={"items": execution.result.items, "aggregations": execution.result.aggregations, "statistics": repr(execution.result.statistics) if args.statistics else None}
        print(json.dumps(output,indent=2 if args.pretty else None,default=str)); return 0
    summary = StringIO()
    result=UnifiedIntelligenceVerticalSlice().run((_source(args.command, args.identifier),), output=summary)
    payload={"execution_id": result.profile.execution_metadata.execution_id, "project": result.profile.canonical_project_identifier, "confidence": result.profile.confidence, "runtime_state": result.runtime.execution.final_state.value, "graph_nodes": len(result.runtime.graph.nodes), "trace": result.profile.traceability}
    if args.json: print(json.dumps(payload, indent=2 if args.pretty else None, default=str))
    else: print(result.console_summary)
    return 0
if __name__ == "__main__": raise SystemExit(main())
