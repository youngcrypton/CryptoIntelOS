# Canonical Relationship Framework

Epic D defines immutable, source-agnostic relationship contracts between canonical entities. A relationship is a first-class typed edge; this package does not infer, resolve, or store edges.

## Philosophy and model

`Relationship` records source and target entities, a canonical `RelationshipType`, category, direction, normalized strength, optional confidence, evidence references, creation time, metadata, and provenance. `RelationshipContext` preserves source, collector, analyzer, timestamp, and policy version. `RelationshipMetadata` carries discovery details, evidence counts, tags, labels, and a version.

Categories group edges by structural, organizational, financial, technical, social, community, governance, security, and infrastructure concerns. Direction explicitly describes support, directed, undirected, or bidirectional semantics. Strength is a normalized weak-to-very-strong scale with unknown available when no assessment exists.

## Future compatibility

The contracts can map directly to graph nodes and typed edges while retaining explainability through provenance and evidence references. Entity-resolution systems can supply canonical endpoints independently. Correlation and AI reasoning components can consume category, direction, strength, confidence, and provenance without coupling to a graph implementation or imposing inference policy. Versioned metadata and policy context allow relationships to be revised and audited over time.

`RelationshipRegistry` is a protocol for future storage or plugin registries only; it contains no implementation logic.
