from dataclasses import dataclass

from .evidence_reference import EvidenceReference
from .evidence_trace import EvidenceTrace


@dataclass(frozen=True, slots=True)
class EvidenceGroup:
    group_key: str
    evidence_type: str
    source: str
    timestamp: str
    references: tuple[EvidenceReference, ...]
    traces: tuple[EvidenceTrace, ...]
