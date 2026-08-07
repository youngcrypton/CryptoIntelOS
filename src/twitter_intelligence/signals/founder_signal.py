from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule

class FounderSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Founder Worth Watching", ("Active Founder",), ("Founder Credibility",), "medium", "Track founder activity and follow-through."))
