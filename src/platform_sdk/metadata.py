"""Immutable metadata contracts for source integrations."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class IntegrationMetadata:
    collector: str
    source: str
    adapter: str
    version: str
    capabilities: tuple[str, ...] = ()
    supported_entity_types: tuple[str, ...] = ()
    supported_observation_types: tuple[str, ...] = ()
