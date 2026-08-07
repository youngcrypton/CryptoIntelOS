# Platform Integration SDK v1.0

## SDK philosophy

The Platform Integration SDK is an internal contract package for source applications. It removes repeated boundary code while leaving the Kernel and Runtime authoritative. The SDK contains no collector implementation, source logic, business rules, provider, scheduler, queue, or execution engine.

The dependency direction is inward: SDK contracts may reference Kernel and Runtime contracts; Kernel and Runtime must never import the SDK. Applications depend on the SDK and provide source-specific implementations outside it.

## Integration lifecycle

Every source follows the immutable lifecycle sequence:

`initialize → collect → translate → execute → shutdown`

Collection produces canonical observations. Translation produces evidence, findings, assessments, and signals. The Runtime façade delegates the already-defined canonical output to the existing Runtime entry point. The SDK does not execute stages itself.

## Adapter pattern

An application owns its source models and implements `SourceAdapter[SourceObject]`. The adapter preserves source identifiers, timestamps, checksums, confidence, and provenance while producing a Kernel `Observation`. The SDK deliberately does not import GitHub, Twitter, website, wallet, blockchain, Discord, or Telegram models.

## Translation pipeline

Typed translator protocols describe the canonical sequence:

`Observation → Evidence → Finding → Assessment → Signal`

Each translator is independently replaceable and testable. Validation protocols accept the canonical model for each stage and return a structured validity result; they define no business rules or source-specific thresholds.

## Runtime integration

`RuntimeFacade` is a thin delegation boundary. It accepts the canonical output tuple and a Runtime context, then invokes an injected Runtime entry point. This preserves Runtime ownership of compilation, execution, graph, correlation, reasoning, automation, and distribution.

## Metadata

`IntegrationMetadata` describes collector, source, adapter, semantic version, capabilities, supported entity types, and supported observation types. Applications should publish this metadata with their registration/configuration and keep it compatible with the Kernel and Runtime major versions they target.

## Extension guide

1. Define source models in the source application package.
2. Implement `SourceCollector` to return canonical observations or source objects with an adapter boundary.
3. Implement `SourceAdapter` and the four translation protocols.
4. Implement validators for the canonical objects.
5. Publish `IntegrationMetadata` and the canonical lifecycle.
6. Inject the existing Runtime entry point through `RuntimeFacade`.
7. Add contract tests for metadata, ordering, provenance, failure propagation, and imports.

## Developer workflow

SDK changes must remain source agnostic, preserve the Kernel → Runtime dependency direction, pass compile/import checks, and include focused protocol-contract tests. Source integrations should not add SDK imports to Kernel or Runtime. New source behavior belongs in the application and adapter packages.
