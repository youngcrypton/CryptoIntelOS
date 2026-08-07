from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel

from .chain_reference import ChainReference


@dataclass(frozen=True, slots=True)
class Address(SerializableModel):
    value: str
    chain: ChainReference | None = None
    label: str | None = None
