from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class Token(SerializableModel):
    token_id: str
    symbol: str
    name: str | None = None
    decimals: int | None = None
