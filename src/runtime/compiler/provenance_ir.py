from dataclasses import dataclass
from datetime import datetime
@dataclass(frozen=True, slots=True)
class ProvenanceIR:
    source: str
    reference: str
    observed_at: datetime | None = None
    metadata: tuple[tuple[str, str], ...] = ()
