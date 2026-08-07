from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class StakingPosition(SerializableModel):
    position_id: str
    owner: str
    asset: str
    amount: str
    validator: str | None = None
