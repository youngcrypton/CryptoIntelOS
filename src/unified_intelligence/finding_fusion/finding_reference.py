from dataclasses import dataclass

from src.core_intelligence.models import Finding


@dataclass(frozen=True, slots=True)
class FindingReference:
    finding_id: str
    source: str
    finding: Finding
