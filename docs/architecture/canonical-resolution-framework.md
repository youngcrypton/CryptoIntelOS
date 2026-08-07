# Canonical Resolution Framework

The resolution framework defines explainable, source-agnostic contracts for deciding how canonical objects relate to one another. It contains no matching, heuristic, AI, graph, or business logic.

## Request lifecycle

`ResolutionRequest` identifies a resolution type and carries submitted objects, creation time, and metadata. Future strategies registered through `ResolutionRegistry` may inspect a request under a `ResolutionContext`, which records execution id, source, policy, and timestamp. A strategy can describe possible outcomes as `ResolutionCandidate` values, each supported by explicit `ResolutionEvidence` and provenance. A `ResolutionDecision` records status, confidence, selected and rejected candidates, reasoning, policy version, and timestamp.

## Policies, provenance, and explainability

`ResolutionPolicy` is a versioned declarative configuration with strict, balanced, aggressive, and manual-review modes. `ResolutionStrategy` names a versioned pluggable approach, including exact, identifier, evidence, AI-assisted, and graph-assisted strategies. Evidence references and explanations remain separate from candidates so every decision can be audited and reproduced without embedding source-specific assumptions.

## Future compatibility

The contracts can be persisted beside Knowledge Graph nodes and edges, preserving decision provenance and policy versions. Entity, relationship, evidence, finding, assessment, and signal resolution all use the same lifecycle. AI reasoning may consume candidates, evidence, confidence, and reasoning fields or propose new candidates through a plugin, while the framework remains responsible only for stable language and traceability.
