# Runtime Path Consolidation

## Canonical execution flow

All supported orchestration follows one flow:

1. Source Intelligence
2. Platform SDK canonical projection
3. Runtime
4. Compiler
5. Knowledge Graph
6. Correlation
7. Reasoning
8. Automation
9. Distribution
10. Execution Result

Applications and compatibility code enter through Platform SDK. Runtime owns stage ordering and lifecycle completion. Application adapters may collect, analyze, or translate data, but they do not construct or execute a separate Runtime pipeline.

## Consolidated paths

The GitHub Runtime integration previously constructed and executed `ExecutionEngine` directly. It now submits its canonical observation, evidence, finding, assessment, and signals through the Platform SDK synchronous gateway. Its `execution` attribute remains as a compatibility property backed by the canonical Runtime result.

The legacy scheduler pipeline, legacy intelligence pipelines, collector orchestrator, and collector execution method remain importable. Their orchestration is deprecated and redirected by `LegacyExecutionAdapter`, which preserves the legacy return value, projects an audit observation, and invokes the canonical Runtime lifecycle through Platform SDK.

## Deprecated orchestration paths

- `src.scheduler.scheduler.Scheduler`
- `src.pipeline.pipeline.IntelligencePipeline`
- `src.pipeline.intelligence_pipeline.IntelligencePipeline`
- `src.intelligence.pipeline.IntelligencePipeline`
- `src.orchestrator.orchestrator.IntelligenceOrchestrator`
- `src.orchestrator.scheduler.Scheduler`
- `BaseCollector.execute`
- `GitHubRuntimeResult.execution` as a standalone execution product

These interfaces are compatibility surfaces, not independent orchestration engines. Deprecation warnings are emitted where calls can be migrated without breaking imports.

## Compatibility adapters

`LegacyExecutionAdapter` supports legacy collectors and processed values. It invokes existing legacy processing callbacks once, preserves their return values, creates a traceable compatibility observation, and delegates execution through `execute_synchronously`. It does not reproduce intelligence business logic inside Runtime.

## Migration strategy

New integrations should translate source output directly to `CanonicalOutput`, create canonical `ExecutionContext`, and use Platform SDK. Existing callers should migrate from scheduler or pipeline globals to source-specific adapters, then replace `LegacyExecutionResult.value` consumption with canonical Runtime outputs. Public legacy interfaces must be removed only in a separately approved breaking release.

## Future distributed execution

Distributed workers, queues, schedules, and remote providers should submit the same canonical projection and execution context through a future Platform SDK transport. Distribution changes where Runtime executes, not its contracts, stage ordering, lifecycle, or role as the sole orchestration engine.
