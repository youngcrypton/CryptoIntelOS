from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class Delegation(SerializableModel):
    delegation_id: str
    delegator: str
    delegate: str
    asset: str
    amount: str
