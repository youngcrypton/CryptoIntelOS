from dataclasses import dataclass
from .graph_edge import GraphEdge
from .graph_node import GraphNode
@dataclass(frozen=True, slots=True)
class GraphProjection:
    nodes: tuple[GraphNode, ...] = ()
    edges: tuple[GraphEdge, ...] = ()
