from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class Transfer(SerializableModel):
    transfer_id: str
    sender: str
    recipient: str
    asset: str
    amount: str
