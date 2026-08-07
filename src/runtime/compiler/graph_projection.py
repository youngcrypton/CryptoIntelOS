from dataclasses import dataclass
from .edge_ir import EdgeIR
from .node_ir import NodeIR
from .timeline_ir import TimelineIR
@dataclass(frozen=True, slots=True)
class GraphProjection:
    nodes: tuple[NodeIR, ...] = ()
    edges: tuple[EdgeIR, ...] = ()
    timeline: TimelineIR | None = None
