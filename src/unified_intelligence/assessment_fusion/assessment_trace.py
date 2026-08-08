from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AssessmentTrace:
    assessment_id: str
    source: str
    supporting_findings: tuple[str, ...]
    supporting_evidence: tuple[str, ...]
    trace_key: str
