from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule

class HiringSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Hiring Wave", ("Hiring Activity",), ("Team Visibility",), "medium", "Track hiring momentum and role concentration."))
