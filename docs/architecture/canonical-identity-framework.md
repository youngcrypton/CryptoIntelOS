# Canonical Identity Framework

Epic C introduces source-agnostic contracts for representing real-world entities across CryptoIntel OS intelligence sources.

## Models

`Entity` is the stable domain object, identified by a UUID and an `EntityType`. It may reference one canonical `Identity`. `Identity` names that object and groups its immutable external `Identifier` values. An identifier carries an `IdentifierType` and optional `IdentityContext` provenance (source, timestamp, record id, and metadata).

`Relationship` is a typed edge between subject and object entities (or their UUIDs), with a `RelationshipType` and optional provenance. `IdentityRegistry` is a protocol only; implementations may register and retrieve entities in a later phase.

## Design rationale

Identity is deliberately separate from observations and evidence. Identifiers can be contributed independently by GitHub, X, Discord, Telegram, wallet, or other adapters without coupling this package to any source implementation. Frozen, slotted dataclasses provide stable, immutable value contracts; tuples preserve identifier collections without prescribing storage or resolution behaviour.

## Future compatibility

Entity Resolution can consume identifiers and contexts to propose or confirm canonical identities while preserving provenance. A Knowledge Graph can persist entities and relationships as nodes and typed edges, attach evidence externally, and evolve its storage independently. No matching, normalization, heuristics, or graph algorithms are included here, so future correlation and AI reasoning components can build on these contracts without redesign.
