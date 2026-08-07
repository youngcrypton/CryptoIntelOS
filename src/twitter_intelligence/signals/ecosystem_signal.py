from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule

class EcosystemSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Ecosystem Breakout", ("Ecosystem Expansion",), ("Ecosystem Presence",), "high", "Monitor ecosystem adoption and integrations."))
