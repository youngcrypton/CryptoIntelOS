from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class BlockReference(SerializableModel):
    block_id: str
    height: int | None = None
    timestamp: str | None = None
