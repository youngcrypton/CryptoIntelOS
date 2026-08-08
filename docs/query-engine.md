# Intelligence Query Engine

The Query Engine is an in-memory deterministic execution layer over existing canonical models, profiles, graph projections, wallets, repositories, websites, and on-chain objects. Immutable queries compile into explicit plans containing ordered predicates, projection fields, and relationship traversals. Runtime, SDK, providers, and canonical ownership are unchanged.

Execution applies equality/membership predicates first, then remaining filters, stable sorting/ranking, aggregation, projection, and pagination. `RelationshipGraph` traverses typed adjacency edges with bounded depth. The local immutable cache keys queries by deterministic hash and records expiration and execution metadata.
