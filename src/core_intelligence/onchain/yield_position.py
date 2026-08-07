from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class YieldPosition(SerializableModel):
    position_id: str
    owner: str
    strategy: str
    principal: str
    accrued: str | None = None
