from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class ChainReference(SerializableModel):
    chain_id: str
    network: str | None = None
    namespace: str | None = None
