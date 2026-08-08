# Architecture

CryptoIntel OS uses a canonical, provider-isolated intelligence pipeline:

```mermaid
flowchart LR
    EXT[External Service] --> C[Connector] --> P[Provider] --> A[Adapter]
    A --> SDK[Platform SDK] --> PR[Production Runtime] --> RT[Runtime]
    RT --> COMP[Compiler] --> KG[Knowledge Graph] --> CORR[Correlation]
    CORR --> REASON[Reasoning] --> AUTO[Automation] --> DIST[Distribution]
    DIST --> PROFILE[Project Intelligence Profile] --> QUERY[Query Engine]
```

## Ownership and boundaries

- `src/core_intelligence` owns canonical business contracts.
- Connectors communicate with external systems but do not create canonical models.
- Providers normalize connector output but do not create canonical models.
- Adapters are the only provider layer allowed to create canonical Kernel objects.
- Platform SDK validates canonical projections and is the supported Runtime entry.
- Runtime owns compiler, graph, correlation, reasoning, automation, distribution, and execution results.
- Production Runtime contracts wrap lifecycle, durability, events, persistence, observability, and provider infrastructure without replacing Runtime.
- Unified Intelligence links identities and fuses intelligence into project profiles.
- Query Engine reads existing models and profiles without changing canonical ownership.

## Architecture rules

Do not bypass adapters, Platform SDK, or Runtime. Do not introduce duplicate canonical contracts, circular dependencies, or a second orchestration engine. Preserve identifiers, provenance, traceability, confidence, timestamps, and execution metadata at every boundary.

## Detailed documentation

- [Architecture documentation](docs/architecture/)
- [Runtime canonical projection](docs/architecture/runtime-canonical-projection.md)
- [Runtime path consolidation](docs/architecture/runtime-path-consolidation.md)
- [Production Runtime](docs/architecture/production-runtime.md)
- [Provider Ecosystem](docs/architecture/provider-ecosystem.md)
- [Repository health](docs/architecture/repository-health.md)
- [System integration](docs/system-integration.md)
- [Query Engine](docs/query-engine.md)
