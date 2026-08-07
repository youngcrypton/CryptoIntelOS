# Canonical Intelligence Model

## Purpose

The canonical intelligence model is the stable, source-agnostic language used by CryptoIntel OS. It separates collected source data from normalized facts, interpretations, scores, and actionable outputs. Collectors and source integrations translate into these contracts; downstream systems consume them without depending on source-specific schemas.

## Canonical models

- **Entity** represents a real-world object. Its stable identifier, aliases, and external identifiers allow future entity-resolution systems to merge observations without changing historical intelligence.
- **Observation** is an immutable record of raw information collected from a source. It is the only canonical model permitted to contain an external raw payload.
- **Evidence** is a normalized fact extracted from an observation. Its observation reference and provenance retain the fact's audit trail.
- **Finding** is an explainable interpretation of one or more evidence records. Its evidence references make the interpretation reproducible.
- **Assessment** is a scored, policy-driven view of an entity. Policy name and version preserve reproducibility when policies evolve.
- **Signal** is actionable intelligence. It includes a recommendation, explanation, severity, confidence, and the evidence supporting the action.

## Intelligence lifecycle

```text
Observation
    |
    v
Evidence
    |
    v
Finding
    |
    v
Assessment
    |
    v
Signal
```

Each stage is produced only after the preceding stage. Evidence must identify its originating observation. Findings, assessments, and signals must retain non-empty evidence references, allowing clients to trace every output to normalized facts and then to raw observations. Pipeline orchestration will enforce ordering; these contracts intentionally contain no workflow or analysis logic.

## Design principles and decisions

The models are frozen, slotted dataclasses. Frozen instances prevent field reassignment and tuple-based reference collections prevent accidental list mutation. Payload and metadata values remain JSON-compatible so records can cross storage and API boundaries. `to_dict()` produces dictionaries with ISO 8601 timestamps for serialization.

Identifiers and classifications are strings rather than closed enums. This permits new entity, source, metric, finding, assessment, signal, severity, and lifecycle types without requiring a breaking contract release. References are identifiers rather than nested models, supporting append-only storage, independent persistence, graph edges, and lightweight AI context.

Confidence and score values are represented as floats but are not constrained by the contracts. Their scales and validation belong to future versioned policies, not the canonical data layer. Structural validation is limited to required evidence relationships.

## Future compatibility

New optional fields may be added with defaults while preserving existing consumers. Meaningful semantic changes require a new contract version and migration guidance. Flexible metadata and provenance mappings allow forward-compatible annotations, but raw source data remains confined to observations.

The identifier-based relationships map naturally to knowledge-graph nodes and edges. Entity aliases and external identifiers provide inputs for future resolution without embedding resolution decisions. Policy versions, collector versions, source versions, checksums, timestamps, and provenance support historical replay and auditability.

Future collectors, analyzers, correlation engines, reasoning systems, and clients should import these contracts rather than define source-specific equivalents. This sprint does not migrate existing implementations or introduce entity resolution, orchestration, scoring, correlation, or signal rules.
