from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from .provenance_ir import ProvenanceIR
@dataclass(frozen=True, slots=True, kw_only=True)
class NodeIR:
    node_id: UUID
    entity_reference: UUID | str
    node_type: str
    labels: tuple[str, ...] = ()
    properties: tuple[tuple[str, str], ...] = ()
    provenance: tuple[ProvenanceIR, ...] = ()
    timestamp: datetime | None = None
