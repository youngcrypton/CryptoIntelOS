from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class TokenBalance(SerializableModel):
    owner: str
    token_id: str
    amount: str
    as_of: str | None = None
