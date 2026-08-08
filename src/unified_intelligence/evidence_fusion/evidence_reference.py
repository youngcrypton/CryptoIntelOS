from dataclasses import dataclass

from src.core_intelligence.models import Evidence


@dataclass(frozen=True, slots=True)
class EvidenceReference:
    evidence_id: str
    source: str
    evidence: Evidence
