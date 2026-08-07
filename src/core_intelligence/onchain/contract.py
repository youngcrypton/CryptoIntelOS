from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel

from .chain_reference import ChainReference


@dataclass(frozen=True, slots=True)
class Contract(SerializableModel):
    contract_id: str
    address: str
    chain: ChainReference
    name: str | None = None
