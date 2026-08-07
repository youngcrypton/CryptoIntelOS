from dataclasses import dataclass
from .graph_edge import GraphEdge
from .graph_node import GraphNode
@dataclass(frozen=True, slots=True)
class GraphResult:
    nodes: tuple[GraphNode, ...] = ()
    edges: tuple[GraphEdge, ...] = ()
    metadata: tuple[tuple[str, str], ...] = ()
