from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class Proposal(SerializableModel):
    proposal_id: str
    title: str
    proposer: str
    status: str = "unknown"
