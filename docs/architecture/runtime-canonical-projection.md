# Runtime Canonical Projection Boundary

## Philosophy

Runtime is source-agnostic. Source, collector, adapter, application, and legacy execution objects are normalized before execution and never interpreted inside Runtime. Projection validates structure and preserves identifiers, provenance, traceability, timestamps, and execution metadata without adding business logic or changing semantic meaning.

## Runtime boundary

`src.platform_sdk.RuntimeFacade` is the supported delegation boundary. `src.platform_sdk.execute_synchronously` is the supported synchronous Runtime gateway. Applications supply a `CanonicalOutput` containing one canonical observation and tuples of canonical evidence, findings, assessments, and signals, together with `src.runtime.engine.ExecutionContext`.

The internal `SynchronousRuntime.execute` method remains available for SDK delegation and defensively rejects non-canonical objects. Application code must not call it directly.

## Supported Runtime contracts

- `src.core_intelligence.models.Observation`
- `src.core_intelligence.models.Evidence`
- `src.core_intelligence.models.Finding`
- `src.core_intelligence.models.Assessment`
- `src.core_intelligence.models.Signal`
- canonical identity information projected as an observation at the compatibility boundary
- `src.runtime.engine.ExecutionContext`

Runtime rejects intelligence-specific DTOs, adapter or provider outputs, collector results, source models, malformed projection tuples, mixed canonical/non-canonical collections, and legacy pipeline execution contexts with an explicit type error.

## Compatibility strategy

Existing Twitter, Website, Wallet, GitHub, Blockchain, and Unified Intelligence integrations remain supported through Platform SDK projections. Unified identity, evidence, finding, and assessment containers are compatibility shims: they project originating canonical records and identity provenance before invoking `RuntimeFacade`. The shims do not pass Unified container types into Runtime and do not recalculate intelligence.

Compatibility projections are intentionally narrow and may be removed only through a separately approved migration. New applications must emit canonical contracts directly.

## Future provider integrations

Future collectors and providers retain source-specific contracts outside Runtime, translate through Platform SDK adapters, preserve source identifiers and provenance, create a canonical execution context, and invoke only a Platform SDK Runtime gateway. Provider-specific parsing, scoring, correlation, or policy decisions do not belong in projection helpers.
