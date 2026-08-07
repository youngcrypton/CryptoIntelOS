from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from .provenance_ir import ProvenanceIR
@dataclass(frozen=True, slots=True, kw_only=True)
class EdgeIR:
    edge_id: UUID
    source_node: UUID | str
    target_node: UUID | str
    relationship_reference: UUID | str
    direction: str
    properties: tuple[tuple[str, str], ...] = ()
    provenance: tuple[ProvenanceIR, ...] = ()
    timestamp: datetime | None = None
