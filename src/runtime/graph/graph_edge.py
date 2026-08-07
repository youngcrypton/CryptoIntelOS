from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src.runtime.compiler import ProvenanceIR
@dataclass(frozen=True, slots=True)
class GraphEdge:
    edge_id: UUID
    source_node: UUID
    target_node: UUID
    relationship_reference: UUID | str
    direction: str
    properties: tuple[tuple[str, str], ...] = ()
    provenance: tuple[ProvenanceIR, ...] = ()
    timestamp: datetime | None = None
