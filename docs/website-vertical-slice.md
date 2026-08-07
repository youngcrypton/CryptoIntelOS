# Website End-to-End Vertical Slice

## Complete execution path

`WebsiteVerticalSlice` provides one synchronous operational path from immutable Website, Page, Document, and Link inputs through discovery, canonical observations, deterministic analysis, assessments, signal generation, compilation, Knowledge Graph projection, correlation, reasoning, automation, distribution planning, and execution completion. It prints a deterministic console summary for every completed stage.

The slice reuses Website Foundation, Discovery, Analysis, and Signal Generation directly. It contains orchestration only and does not duplicate source logic.

## Runtime participation

Discovery creates one canonical batch observation through `WebsiteRuntimeIntegration` and the Platform SDK `RuntimeFacade`. The final observation, evidence, findings, assessments, and signals cross the same SDK boundary into the existing `SynchronousRuntime`. Runtime compiles the canonical objects, projects graph nodes, correlates the execution, performs deterministic reasoning, creates a monitoring automation plan, creates and accepts a console distribution plan, and completes the execution engine pipeline.

Platform, Kernel, Runtime, and Platform SDK implementations remain unchanged.

## Current limitations

- Inputs are supplied synchronously as in-memory Website source models.
- Runtime projections and plans are deterministic and in-memory rather than durable.
- Analysis and signals use explicit deterministic rules rather than external AI inference.
- Console distribution creates an accepted plan but does not publish externally.
- The slice performs no cross-source correlation.

## Future crawler integration

A future crawler can translate fetched pages, documents, and links into the existing immutable Website source contracts before invoking this slice. HTTP retrieval, robots policy, rendering, retries, parsing, and crawl scheduling remain outside this orchestration boundary.

## Future real-time monitoring

Real-time monitoring can submit normalized resource batches to the same execution path. Durable queues, snapshot comparison, change detection, idempotency, checkpointing, and replay can wrap the source boundary without changing canonical models or Runtime contracts.
