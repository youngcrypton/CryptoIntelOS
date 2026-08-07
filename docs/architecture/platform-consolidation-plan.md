# Platform Consolidation & Integration — Phase 2.1

## Scope and audit basis

This document inventories the repository as it exists at the start of Phase 2.1. It is an analysis artifact only. No code, configuration, or architecture has been changed as part of this phase.

The repository contains approximately 49 test files and several parallel implementations of domain concepts. The most important finding is that the documented Runtime/Kernel architecture is not yet the architecture exercised by the application.

## 1. Canonical model inventory

| Concept | Current representations | Preferred canonical candidate | Decision |
|---|---|---|---|
| Entity | `src/core_intelligence/models.py:Entity`; `src/core_intelligence/identity/entity.py:Entity`; GitHub `Repository`, `Organization`, `Contributor` | `core_intelligence` identity Entity, extended by source adapters | Identity package should become canonical. The flat model must be adapted/deprecated. |
| Observation | `src/core_intelligence/models.py:Observation`; `src/models/*Snapshot`; `CollectorResult` | `core_intelligence.models.Observation` | Canonical candidate. Snapshot records become persistence/source adapters. |
| Evidence | `src/core_intelligence/models.py:Evidence`; `src/core_intelligence/evidence.py:IntelligenceEvidence`; `runtime.correlation.EvidenceBundle`; GitHub analyzer outputs | `core_intelligence.models.Evidence` | Canonical evidence record; bundles are runtime transport/grouping objects. |
| Finding | `src/core_intelligence.models.Finding`; `src/intelligence/finding.py:Finding`; `AnalyzerResult`/rule findings | `core_intelligence.models.Finding` | Canonical interpretation contract; legacy findings adapt into it. |
| Assessment | `src/core_intelligence.models.Assessment`; `RepositoryScore`; `ProjectIntelligenceProfile`; `LivingIntelligenceProfile` | `core_intelligence.models.Assessment` | Canonical assessment envelope; domain scores remain typed source-specific components. |
| Signal | `src/core_intelligence.models.Signal`; `src/intelligence/core/signal.py`; `src/models/intelligence_signal.py`; `intelligence_core.models.IntelligenceSignal`; two GitHub signal models | `core_intelligence.models.Signal` | One canonical signal contract is mandatory. All other signal types become adapters or are deprecated. |
| Relationship | `src/core_intelligence/relationships/relationship.py`; `src/core_intelligence/identity/relationship.py`; `runtime.graph.GraphEdge`; `runtime.correlation.GraphBundle` | `core_intelligence.relationships.Relationship` | Relationship package should own semantic relationships; graph edges are projection records. |
| Identity | `src/core_intelligence/identity/*`; GitHub identity/profile models; `Project` | `core_intelligence.identity` | Canonical identity and identifier registry. GitHub/source identities remain adapters. |
| Memory | `src/core_intelligence/memory/*`; `runtime.reasoning.ReasoningMemory`; `runtime.automation.AutomationContext`; database snapshots | `core_intelligence.memory` for durable memory contracts | Reasoning memory is a specialized adapter/view; contexts are not memory. |
| Policy | `src/core_intelligence/policy/*`; runtime compiler/correlation/reasoning/automation/distribution policies; config rules | Kernel policy envelope plus typed subsystem policies | Kernel owns policy identity/version/scope. Runtime policies must be subordinate typed policy payloads. |
| Execution context | `src/orchestrator/execution_context.py`; `src/core_intelligence/interfaces/context.py:ExecutionContext`; `src/runtime/engine/execution_context.py:ExecutionContext` | Runtime engine execution context | Orchestrator context becomes an adapter; Kernel interface context must be renamed or unified. |
| Runtime context | compiler, graph, correlation, reasoning, automation, and distribution contexts | Shared runtime context envelope plus subsystem views | Current contexts are fragmented. A single correlation/execution identity and timestamp policy is required. |

### Canonicalization rule

Canonical objects must be immutable, serializable, versioned, provenance-bearing, timezone-safe, and independent of source/provider packages. Current frozen dataclasses are only shallowly immutable because many contain mutable mappings or arbitrary `object` values.

## 2. Duplicate models and disposition

| Duplicate concept | Why it exists | Disposition |
|---|---|---|
| Entity (`models.py` vs `identity/entity.py`) | Initial flat intelligence contracts and later identity framework were developed independently | Keep identity Entity; create explicit flat-model adapter; deprecate duplicate. |
| Relationship (identity vs relationships packages) | Identity relationship and semantic relationship concerns were split without a single owner | Keep semantic relationships package and fold identity linkage into it or define a strict identity-edge subtype. |
| Signal (core, models, intelligence_core, two GitHub stacks) | Features were implemented before Kernel adoption and GitHub evolved separately | Keep one Kernel Signal; adapt GitHub and legacy signals; deprecate duplicate public models. |
| Finding (`core_intelligence` and `intelligence`) | Rule engine predates canonical Kernel | Keep Kernel Finding; convert rule results. |
| Assessment (`core_intelligence.Assessment`, repository scores, profiles) | Scoring was built as application/domain output rather than canonical assessment | Keep Kernel envelope; preserve score explanations as evidence/reasoning payloads. |
| ExecutionContext (orchestrator, core interfaces, runtime engine) | Each phase introduced its own lifecycle context | Keep Runtime context; use adapters at collectors and orchestration boundaries. |
| IntelligencePipeline (top-level pipeline and `intelligence.pipeline`) | Multiple prototypes and release phases | Keep one application adapter and one Runtime pipeline; deprecate the other after migration. |
| CollectorRegistry (collectors and orchestrator) | Local registration needs were implemented twice | Keep one registry protocol plus implementation; source catalogs supply registration metadata. |
| Signal engine (GitHub root and `github_intelligence.signals`) | Two GitHub signal implementations were introduced in parallel | Select one implementation, wrap its outputs in canonical Signal, archive the other. |
| Snapshot models (`src/models` and core observations) | Persistence tables were modeled directly | Keep storage records private to repositories; map to Observation. |
| Reasoning memory vs Kernel memory | AI reasoning needed local context | Keep as a bounded reasoning view backed by Kernel memory references. |

## 3. Runtime inventory

| Component | Public API | Dependencies | Current consumers | Future consumers |
|---|---|---|---|---|
| Compiler | `Compiler.compile(objects, context)` | compiler context/result, graph projection/IR | Tests and package imports; no application path | Canonical object-to-graph/timeline compilation |
| Execution | `ExecutionEngine.initialize/execute/shutdown`; execution contracts | runtime pipeline, stages, state/events | Runtime tests; not orchestrator | Durable worker/runtime coordinator |
| Graph | `GraphBackend.query/supports`, `GraphAdapter`, `Graph`, projection/query/result contracts | compiler provenance IR and graph contracts | Tests/package imports; no concrete backend | Neo4j/property graph/search projections |
| Correlation | `CorrelationEngine.correlate(strategy, objects, context)` and rule/policy/result contracts | runtime-only correlation objects | Tests; no collector/application consumer | Cross-source evidence correlation |
| Reasoning | `ReasoningEngine.reason(strategy, request, context)`; provider/registry/strategy protocols | reasoning contracts | Tests; no provider implementation | Hosted/local models, RAG, replayable reasoning |
| Automation | `AutomationEngine.decide(context, policy, strategy_name)` | automation policy/registry/strategy/plan/result | Tests; no application consumer | Action-plan generation from canonical signals |
| Distribution | `DistributionEngine.distribute(plan, context, strategy)` | distribution registry/provider/strategy contracts | Tests; no provider implementation | Provider delivery workers and future transports |

Runtime contracts are internally mostly acyclic, but there is a dependency leak: `runtime.graph.graph_node` imports compiler provenance IR. The more serious problem is absence of consumers; contracts do not establish an integration architecture until a vertical path uses them.

## 4. GitHub inventory

### Source and request layer

- `github_intelligence.client.GitHubClient`, authentication, configuration, and `RateLimiter`
- discovery and filters under `github_intelligence.discovery`
- repository, organization, and contributor discovery helpers

These remain GitHub-specific. They should emit canonical `Observation` objects through a GitHub collector adapter.

### Models

- `github_intelligence.models`: Repository, Organization, Contributor, Commit, Release
- contributor, organization, activity, dependency, and release profile/intelligence dataclasses
- repository analysis and metadata models

These are useful source-domain models, but should not become Kernel models. They should remain behind a GitHub adapter and be referenced in provenance/payloads.

### Analyzers

- commit/activity analyzers
- release analyzer
- contributor analyzer/discovery/profile
- organization analyzer/discovery/profile
- dependency analyzer/records
- repository analyzer, technology detector, metadata extractor, activity analyzer

The analyzers should remain GitHub-specific. Their outputs should be translated to Evidence and Findings; analyzer logic should not move into Runtime.

### Scoring and signals

- `RepositoryScoringEngine`, `RepositoryScore`, `ScoreExplanation`
- `github_intelligence.signal_engine.GitHubSignalEngine`
- `github_intelligence.signals.signal_engine.SignalEngine`
- `signals.signal_models` and `signals.signal_rules`

Scoring heuristics remain GitHub-specific. Score explanations, evidence references, and generated signals should migrate through a canonical adapter. The duplicate signal engines must be consolidated before migration.

### Migration boundary

Migrate the collector/output boundary, provenance, evidence references, confidence, and explainable signal envelope. Keep GitHub API models, rate limiting, pagination, repository heuristics, and source taxonomy inside the GitHub plugin.

## 5. Dependency graph

### Intended direction

```text
Kernel contracts
        ↓
Runtime contracts/orchestration
        ↓
Source adapters (GitHub, X, websites, future sources)
        ↓
Persistence, graph, AI, and distribution providers
        ↓
Application/API/UI composition
```

### Current effective direction

```text
src.core / orchestrator
  → collectors / discovery / services
  → intelligence rules and pipelines
  → repositories / SQLite

src.runtime  (mostly isolated contracts)
src.core_intelligence (partly canonical, partly isolated)
src.github_intelligence (source-specific parallel domain)
```

### Violations and coupling risks

- `core_intelligence.relationships.relationship` imports identity implementation directly instead of depending on a stable identity interface.
- Runtime graph imports compiler IR, coupling two Runtime subsystems at model level.
- `core_intelligence.intelligence_space` imports canonical models through package re-exports, increasing import coupling.
- Services import concrete collectors directly, bypassing collector protocols.
- Scheduler/orchestrator import concrete/global registries.
- Factory and registry mappings are hardcoded rather than plugin-loaded.
- Multiple pipeline and registry implementations make dependency ownership ambiguous.
- Database manager is a process-global SQLite singleton.
- GitHub is not downstream of Runtime/Kernel; it has its own model and signal graph.

No obvious direct import cycle was found in the audited packages, but the architecture has cycle risk because package `__init__` files re-export many concrete models and several layers import those package-level re-exports.

## 6. Migration plan

1. **Freeze the inventory and ownership decisions.** Publish one canonical model table and prohibit new duplicate domain models.
2. **Select and consolidate canonical Kernel objects.** Resolve Entity, Relationship, Signal, Finding, Assessment, and context ownership first; add schema/version identifiers.
3. **Define adapters and deprecation policy.** Every legacy model gets an explicit conversion boundary, test fixture, and removal owner.
4. **Define serialization and persistence contracts.** Establish timestamps, IDs, provenance, schema compatibility, migration versions, retention, and idempotency.
5. **Build a canonical observation ingestion slice.** Convert one GitHub repository response into Observation and persist it durably.
6. **Map GitHub analyzer outputs.** Convert analyzer outputs into Evidence, Findings, Assessments, and Signals without moving GitHub heuristics into Runtime.
7. **Consolidate GitHub signal engines.** Select one rule engine and add a canonical Signal adapter.
8. **Implement Runtime execution lifecycle.** Add real stage dispatch, failure states, retries, cancellation, correlation IDs, and durable execution records.
9. **Connect correlation, graph, and reasoning.** Use canonical objects and explicit adapters; add replayable context and provenance.
10. **Connect automation and distribution.** Generate plans from canonical Signals, then deliver through provider plugins.
11. **Replace local orchestration with workers/events.** Introduce queue/event semantics, checkpoints, backpressure, and dead-letter handling.
12. **Load-test and fault-test before broad source migration.** Validate throughput, replay, duplicates, provider failure, and schema evolution.

This order minimizes the risk of migrating GitHub into a moving target. Model ownership and durability must precede Runtime integration.

## 7. Consolidation plan

| Current component | Canonical component | Migration strategy | Risk | Recommended action |
|---|---|---|---|---|
| `core_intelligence.models.Entity` | `core_intelligence.identity.Entity` | Adapter + validation | High | Deprecate flat Entity after consumers migrate |
| `src/models/*Snapshot` | Kernel Observation + repository record | Mapper at persistence boundary | High | Keep storage records private |
| GitHub Repository/Commit/Release models | Observation/Evidence payloads | Source adapter | Medium | Keep GitHub models source-local |
| `intelligence.core.Signal` | Kernel Signal | Field mapper | High | Deprecate after rule migration |
| `models.intelligence_signal` | Kernel Signal | Field mapper | High | Remove duplicate public API |
| GitHub signal engines | Kernel Signal + Runtime correlation/automation inputs | Select one, wrap output | High | Consolidate before GitHub Runtime migration |
| `intelligence.finding.Finding` | Kernel Finding | Adapter | Medium | Migrate rule engine output |
| `RepositoryScore` | Kernel Assessment | Preserve explanation as evidence/reasoning | Medium | Keep scoring algorithm GitHub-specific |
| `orchestrator.ExecutionContext` | Runtime engine context | Adapter | High | Stop creating new orchestrator context fields |
| `core_intelligence.interfaces.ExecutionContext` | Runtime execution context | Rename/compatibility alias | High | Establish one context envelope |
| `runtime.engine.ExecutionContext` | Shared Runtime context | Canonicalize IDs/time/schema | Medium | Make it the runtime owner |
| `collectors.CollectorRegistry` | One registry protocol/implementation | Adapter and remove singleton use | Medium | Use dependency injection |
| `orchestrator.CollectorRegistry` | One registry protocol/implementation | Adapter | Medium | Deprecate duplicate |
| top-level `pipeline.IntelligencePipeline` | Runtime pipeline | Vertical migration | High | Keep façade during transition |
| `intelligence.pipeline.IntelligencePipeline` | Runtime pipeline stages | Adapter | High | Remove duplicate pipeline ownership |
| SQLite `DatabaseManager` | Persistence ports + production backend | Repository adapter/migration | Critical | Introduce migrations and durable backend |

## 8. Technical debt

### Critical

- No single canonical model authority.
- Runtime is disconnected from the application path.
- SQLite/local singleton persistence cannot support target scale.
- No durable event, checkpoint, replay, or idempotency semantics.
- GitHub contains parallel signal/model systems that will conflict during migration.

### High

- Placeholder Runtime execution/compiler/correlation/reasoning implementations.
- Duplicate registries, pipelines, contexts, signals, and identity models.
- Hardcoded collector factories and source registration.
- No schema registry, migrations, or wire compatibility guarantees.
- No observability, distributed tracing, or operational metrics.
- Inconsistent timezone handling and shallow immutability.
- No concrete graph or AI provider implementations.

### Medium

- Global singletons and concrete imports across services/orchestration.
- Weak typing at subsystem boundaries (`object`, unvalidated mappings).
- Incomplete retry/error taxonomy and resource lifecycle contracts.
- Runtime tests named outside the configured pytest discovery pattern.
- Documentation describes future architecture as if it were implemented.
- No load, fault-injection, security, or migration tests.

### Low

- Mixed formatting and one-line exception/class definitions.
- `print`-based operational output in database/orchestrator paths.
- Duplicate/overlapping package names and legacy compatibility surface.
- No enforced black/isort/flake8/mypy CI gate despite listing those tools.

## Recommended audit conclusion

The repository should enter consolidation, not broad integration. The immediate objective is to make the Kernel genuinely canonical, connect one durable end-to-end source path to Runtime, and remove parallel model ownership. GitHub migration should begin only after those contracts and adapters are tested in a vertical slice.

## Phase 2.2–2.3 migration status

GitHub is the first source plugin with an explicit canonical adapter boundary. Repository metadata becomes an `Observation`; contributor and organization intelligence become `Evidence`; repository analysis becomes a `Finding`; repository scoring becomes an `Assessment`; and GitHub signals become canonical `Signal` objects.

The synchronous integration path uses the existing Runtime execution engine and records collection, analysis, compilation, graph projection, correlation, reasoning, assessment, signal, automation, and distribution stages. It adds no provider, queue, scheduler, persistence implementation, or GitHub heuristic to Runtime.

Canonical ownership remains in `src.core_intelligence.models` for Observation, Evidence, Finding, Assessment, and Signal. GitHub API models and all source-specific analysis/scoring logic remain inside `src.github_intelligence`.

## Phase 2.4 operational vertical slice

The first operational execution is synchronous and uses GitHub as the source application. Existing repository analysis, repository scoring, and GitHub signal rules produce source-specific outputs. The adapter layer converts those outputs into canonical Observation, Evidence, Finding, Assessment, and Signal objects before Runtime participation.

The source-agnostic synchronous Runtime then executes compilation, in-memory graph projection, deterministic correlation, deterministic provider-free reasoning, automation planning, distribution planning, and execution lifecycle recording. The GitHub application renders the resulting console summary; Runtime does not import GitHub.

Current limitations are deliberate: graph state is in-memory, reasoning uses no AI provider, distribution creates an accepted plan without contacting a destination, execution is single-process, and there is no queue, scheduler, persistence migration, retry worker, or distributed checkpoint.

Future distributed execution can replace the synchronous implementations behind the existing Runtime protocols. Canonical object identifiers, execution IDs, plans, contexts, and results provide the hand-off boundary for queues, durable workers, graph providers, AI providers, and delivery providers.
