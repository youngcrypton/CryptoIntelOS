from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProfileSummary:
    sources_linked: int
    evidence_items: int
    project_findings: int
    project_assessments: int
    signals: int
