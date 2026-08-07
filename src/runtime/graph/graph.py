from dataclasses import dataclass
from uuid import UUID
from .graph_projection import GraphProjection
from .graph_version import GraphVersion
@dataclass(frozen=True, slots=True)
class Graph:
    graph_id: UUID
    version: GraphVersion
    projection: GraphProjection
