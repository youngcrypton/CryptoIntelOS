# Twitter End-to-End Vertical Slice

## Complete execution path

`TwitterVerticalSlice` provides one synchronous operational path:

1. Accept a Twitter profile and one or more source-specific posts.
2. Discover canonical profile and post observations with the Twitter Discovery Engine.
3. Aggregate discovery through the Platform SDK boundary into a deterministic batch observation.
4. Analyze each discovered observation into canonical evidence, findings, and assessments.
5. Generate canonical signals from each complete analysis chain.
6. Forward the combined canonical output through `TwitterRuntimeIntegration` and the Platform SDK `RuntimeFacade`.
7. Execute the existing synchronous compiler, Knowledge Graph projection, correlation, reasoning, automation, distribution planning, and execution engine.
8. Print a deterministic summary of every completed stage.

Source discovery, analysis, and signal logic are reused directly; the vertical slice contains orchestration only.

## Runtime participation

The Runtime receives one batch observation plus all canonical evidence, findings, assessments, and signals. `SynchronousRuntime` compiles those objects, projects graph nodes, correlates the execution, performs deterministic reasoning, creates a monitoring automation plan, creates and accepts a console distribution plan, and completes the standard execution pipeline. Runtime, Platform, Kernel, and SDK implementations are unchanged.

## Current limitations

- Input is supplied synchronously as in-memory Twitter profile and post models.
- Collection does not call the Twitter/X API.
- Runtime projections are deterministic and in-memory rather than durable.
- Analysis and signals retain their current explicit keyword-rule limitations.
- The console distribution provider creates an accepted plan but does not publish externally.

## Future API integration

A future collector can translate Twitter/X API responses into the existing `TwitterProfile` and `TwitterPost` contracts before invoking this slice. Authentication, pagination, rate limiting, retries, and API error handling belong at that collector boundary and do not require changes to discovery, analysis, signal generation, or Runtime.

## Future real-time streaming support

Streaming ingestion can submit normalized profile and post batches to the same orchestration path. Durable queues, idempotency storage, checkpointing, backpressure, and replay should wrap the source boundary while preserving canonical identifiers and the synchronous lifecycle demonstrated here.
