from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule


class HiringSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Active Project Hiring", ("Active Hiring",), ("Hiring Activity",), "medium", "Track hiring activity for execution and growth signals."))
