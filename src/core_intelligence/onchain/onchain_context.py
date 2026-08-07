from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel

from .chain_reference import ChainReference


@dataclass(frozen=True, slots=True)
class OnChainContext(SerializableModel):
    source: str
    chain: ChainReference | None = None
    observed_at: str | None = None
    correlation_id: str | None = None
