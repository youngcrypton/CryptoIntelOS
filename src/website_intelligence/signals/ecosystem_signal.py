from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule


class EcosystemSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Ecosystem Presence", ("Strong Ecosystem Presence",), ("Ecosystem Presence",), "medium", "Validate ecosystem integrations and monitor adoption."))
