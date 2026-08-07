from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class TransactionFee(SerializableModel):
    amount: str
    asset: str
    payer: str | None = None
