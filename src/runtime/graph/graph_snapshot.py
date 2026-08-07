from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from .graph_projection import GraphProjection
from .graph_version import GraphVersion
@dataclass(frozen=True, slots=True)
class GraphSnapshot:
    snapshot_id: UUID
    graph_id: UUID
    captured_at: datetime
    version: GraphVersion
    projection: GraphProjection
