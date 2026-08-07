"""Possible outcome of a resolution request."""
from dataclasses import dataclass, field
from uuid import UUID, uuid4
from .resolution_evidence import ResolutionEvidence

@dataclass(frozen=True, slots=True)
class ResolutionCandidate:
    target_reference: str | UUID
    candidate_id: UUID = field(default_factory=uuid4)
    confidence: float | None = None
    supporting_evidence: tuple[ResolutionEvidence, ...] = ()
    metadata: tuple[tuple[str, str], ...] = ()
