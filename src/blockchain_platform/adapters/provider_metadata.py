from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProviderMetadata:
    provider_id: str
    name: str
    version: str
    supported_chains: tuple[str, ...] = ()
    capabilities: tuple[str, ...] = ()
