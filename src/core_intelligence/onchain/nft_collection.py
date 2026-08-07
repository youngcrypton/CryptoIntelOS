from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class NFTCollection(SerializableModel):
    collection_id: str
    name: str
    symbol: str | None = None
