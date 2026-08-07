from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src.runtime.compiler import ProvenanceIR
@dataclass(frozen=True, slots=True)
class GraphNode:
    node_id: UUID
    entity_reference: UUID | str
    labels: tuple[str, ...] = ()
    properties: tuple[tuple[str, str], ...] = ()
    provenance: tuple[ProvenanceIR, ...] = ()
    timestamp: datetime | None = None
