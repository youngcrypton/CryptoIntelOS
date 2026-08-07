from typing import Protocol
from .graph import Graph
from .graph_backend import GraphBackend
from .graph_context import GraphContext
from .graph_projection import GraphProjection
class GraphAdapter(Protocol):
    def project(self, projection: GraphProjection, context: GraphContext) -> Graph: ...
    def backend(self) -> GraphBackend: ...
