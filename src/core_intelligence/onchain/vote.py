from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class Vote(SerializableModel):
    vote_id: str
    proposal_id: str
    voter: str
    choice: str
    weight: str | None = None
