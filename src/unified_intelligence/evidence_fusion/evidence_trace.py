from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvidenceTrace:
    evidence_id: str
    source: str
    origin: str
    trace_key: str
