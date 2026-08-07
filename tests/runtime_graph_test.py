from dataclasses import asdict
from datetime import UTC, datetime
from uuid import UUID
from src.runtime.graph import *
def test_graph_projection_version_and_snapshot():
    node=GraphNode(UUID(int=1), "entity-1", ("Project",))
    edge=GraphEdge(UUID(int=2), node.node_id, UUID(int=3), "relationship-1", "directed")
    projection=GraphProjection((node,), (edge,)); version=GraphVersion("1", datetime.now(UTC), "memory-1")
    graph=Graph(UUID(int=4), version, projection); snapshot=GraphSnapshot(UUID(int=5), graph.graph_id, datetime.now(UTC), version, projection)
    assert snapshot.projection.nodes[0] == node
    assert snapshot.projection.edges[0].source_node == node.node_id
    assert asdict(graph)["version"]["memory_version"] == "memory-1"
def test_query_and_registry_contracts():
    query=GraphQuery(GraphQueryType.NEIGHBORS, (("node_id", "1"),))
    assert query.query_type is GraphQueryType.NEIGHBORS
    assert "register" in GraphRegistry.__dict__
    assert "query" in GraphBackend.__dict__
