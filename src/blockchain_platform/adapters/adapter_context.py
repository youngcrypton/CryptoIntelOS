from dataclasses import dataclass

from src.core_intelligence.onchain import ChainReference


@dataclass(frozen=True, slots=True)
class AdapterContext:
    provider_id: str
    chain: ChainReference
    observed_at: str | None = None
    correlation_id: str | None = None
