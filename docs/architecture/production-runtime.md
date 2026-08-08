# Production Runtime Contracts

This release adds production infrastructure contracts around the existing Runtime pipeline. The processing order and intelligence behavior remain unchanged: Platform SDK → Runtime → Compiler → Knowledge Graph → Correlation → Reasoning → Automation → Distribution.

## Durable execution

`src.runtime.durable` defines immutable jobs, snapshots, checkpoints, contexts, results, lifecycle states, transitions, retry policies, replay, recovery, and manager contracts. `ExecutionStore` and `CheckpointStore` are protocols only; this release provides no database or filesystem persistence.

The lifecycle states are Created, Queued, Running, Paused, Retrying, Completed, Failed, Cancelled, and TimedOut. `LifecycleManager` validates legal transitions, while replay and recovery resume from an explicit checkpoint without mutating historical contracts.

## Lifecycle and events

`LifecyclePolicy`, `RetryPolicy`, and `RetryStrategy` describe deterministic retry and timeout metadata. `src.runtime.events` provides typed runtime event envelopes, metadata carrying execution/correlation/trace IDs, a registry, publisher/subscriber protocols, bus, and dispatcher. Events are in-process abstractions; Kafka, RabbitMQ, and NATS are intentionally out of scope.

## Persistence contracts

`src.runtime.persistence` defines protocol-only stores for executions, events, graph data, evidence, findings, assessments, signals, profiles, and checkpoints. Implementations must be selected later behind these stable interfaces and must preserve canonical identifiers and provenance.

## Observability

The existing `src.runtime.observability` module now includes immutable `Trace`, `Span`, `ExecutionTimeline`, `RuntimeMetrics`, `StructuredLog`, health checks/registry, and OpenTelemetry-compatible protocols without importing a vendor SDK. Metadata supports trace, correlation, execution, stage timing, and structured dimensions.

## Provider infrastructure

`src.runtime.providers` defines provider descriptors, capabilities, status/health, registries, negotiation, monitoring, rate-limiter/backoff/circuit-breaker protocols, and typed results. There is no networking or live provider implementation. Future providers must negotiate capabilities, report health, apply rate limits, preserve provenance, and remain isolated from Runtime business logic.

## Production execution philosophy

Infrastructure wraps the existing deterministic Runtime; it does not replace or redesign it. Contracts are immutable where state must be historical, protocols isolate persistence and provider implementations, and orchestration remains explicit and testable. A production implementation must add durable storage, failure-aware dispatch, idempotency, replay, structured telemetry, and operational controls before unattended operation.

## Future distributed execution

Workers, queues, and remote providers should transport the same `ExecutionJob`, `JobContext`, canonical Runtime projection, event envelope, and checkpoint contracts. Distribution changes placement and durability, not the Runtime processing order or canonical boundary.
