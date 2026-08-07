"""Structural contract for plugin-friendly component registries."""

from typing import Protocol, runtime_checkable

from .components import Analyzer, Collector, Correlator, Resolver, Scorer, SignalGenerator


@runtime_checkable
class ComponentRegistry(Protocol):
    """Register and retrieve canonical intelligence components by name."""

    def register_collector(self, name: str, component: Collector) -> None: ...

    def register_analyzer(self, name: str, component: Analyzer) -> None: ...

    def register_resolver(self, name: str, component: Resolver) -> None: ...

    def register_scorer(self, name: str, component: Scorer) -> None: ...

    def register_signal_generator(self, name: str, component: SignalGenerator) -> None: ...

    def register_correlator(self, name: str, component: Correlator) -> None: ...

    def get_component(self, component_type: str, name: str) -> object: ...
