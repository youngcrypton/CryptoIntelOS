"""Evidence supporting a resolution decision."""
from dataclasses import dataclass
from .resolution_context import ResolutionContext

@dataclass(frozen=True, slots=True)
class ResolutionEvidence:
    evidence_reference: str
    weight: float | None = None
    explanation: str | None = None
    provenance: ResolutionContext | None = None
