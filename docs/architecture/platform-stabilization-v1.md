# Milestone 3 — Platform Stabilization v1.0

## Package responsibilities

`core_intelligence` owns source-agnostic Kernel models and identity, relationship, memory, resolution, and policy contracts. `runtime` owns compilation, execution lifecycle, graph projection, correlation, reasoning, automation, distribution, and observability contracts. `github_intelligence` owns GitHub API access, pagination/rate limits, analyzers, heuristics, scoring, and source adapters. Application packages compose these contracts; they do not redefine canonical objects.

## Dependency rules

1. Kernel packages must not import Runtime, collectors, providers, or GitHub.
2. Runtime packages must not import GitHub, collectors, or destination providers.
3. GitHub-specific code may depend on Kernel contracts only through adapter boundaries.
4. Providers and adapters may depend inward on stable contracts, never the reverse.
5. Package `__init__` files expose public contracts only; implementation helpers remain module-private.
6. New duplicate Entity, Observation, Evidence, Finding, Assessment, Signal, Relationship, Identity, or Memory models are prohibited.
7. Import-graph validation and focused boundary tests are required for changes to these packages.

## Canonical model consolidation

The authoritative operational models are exported from `src.core_intelligence.models` for Observation, Evidence, Finding, Assessment, and Signal, with identity and relationship ownership in `src.core_intelligence.identity` and `src.core_intelligence.relationships`. Legacy finding/signal DTOs are explicitly marked deprecated and remain only for compatibility with the older rule/application path. GitHub models remain source-local and must be adapted before Runtime use.

## Extension and adapter guide

A new source should implement collection and source-domain analysis independently, then add adapters that produce canonical observations and evidence-linked interpretations. Adapters must preserve source identifiers, checksums, timestamps, confidence, and provenance. Runtime and Kernel imports must never point back to the source package. Source heuristics, API pagination, rate limits, and provider-specific fields remain outside the canonical layer.

## Runtime lifecycle

The synchronous lifecycle is: initialize an execution context, compile canonical objects, project an in-memory graph, correlate objects, produce deterministic/provider-backed reasoning, create automation plans, create distribution plans, and record execution state. Runtime observability contracts provide stable execution, correlation, and trace identifiers plus stage timing and counters without implementing a logging system.

## Versioning policy

Kernel, Runtime, Platform, and adapter packages expose semantic `__version__` metadata. Major versions may break public contracts; minor versions add backwards-compatible contracts; patch versions contain compatible fixes. Canonical model schema versions must be independently recorded when serialized. Adapters must declare compatibility with the Kernel and Runtime major versions they target.

## Current limitations

Stabilization does not add persistence migrations, queues, schedulers, external providers, distributed workers, or new intelligence sources. Graph, reasoning, and distribution behavior in the vertical slice remains deterministic/in-memory. These limitations are intentional and must not be mistaken for production-scale implementations.
