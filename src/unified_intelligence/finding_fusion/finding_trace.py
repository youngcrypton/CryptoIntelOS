from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FindingTrace:
    finding_id: str
    source: str
    supporting_evidence: tuple[str, ...]
    trace_key: str
