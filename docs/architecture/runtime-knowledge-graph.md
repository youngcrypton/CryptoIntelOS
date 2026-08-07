# Runtime Knowledge Graph Foundation

The Knowledge Graph is a rebuildable semantic projection of Canonical Intelligence Memory. Memory remains the source of truth; the graph exists for traversal, querying, correlation, and future AI reasoning.

Graph nodes and edges retain canonical entity and relationship references, properties, timestamps, and compiler provenance. `GraphProjection` groups immutable nodes and edges. `GraphVersion` links a graph revision to its source memory version, and `GraphSnapshot` captures a historical point-in-time projection for temporal reconstruction.

Queries and results are backend-independent and contain no Cypher, Gremlin, SPARQL, or persistence semantics. `GraphAdapter`, `GraphBackend`, and `GraphRegistry` protocols isolate future Neo4j, Memgraph, RDF, distributed, or other providers. This abstraction keeps graph state disposable and allows AI traversal without making the graph authoritative.
