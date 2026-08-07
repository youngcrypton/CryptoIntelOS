"""Explainable final resolution outcome."""
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from .resolution_candidate import ResolutionCandidate
from .resolution_status import ResolutionStatus

@dataclass(frozen=True, slots=True, kw_only=True)
class ResolutionDecision:
    decision_id: UUID = field(default_factory=uuid4)
    status: ResolutionStatus
    confidence: float | None = None
    chosen_candidate: ResolutionCandidate | None = None
    rejected_candidates: tuple[ResolutionCandidate, ...] = ()
    reasoning: str | None = None
    policy_version: str | None = None
    timestamp: datetime | None = None
