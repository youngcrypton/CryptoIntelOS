from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class LendingPosition(SerializableModel):
    position_id: str
    owner: str
    market: str
    supplied: tuple[tuple[str, str], ...] = ()
    borrowed: tuple[tuple[str, str], ...] = ()
