from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class LiquidityPool(SerializableModel):
    pool_id: str
    assets: tuple[str, ...]
    protocol: str | None = None
