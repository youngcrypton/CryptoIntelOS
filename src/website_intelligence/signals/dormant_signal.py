from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule


class DormantSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Dormant Website Risk", ("Dormant Website",), ("Identity Confidence",), "high", "Validate project activity through independent sources.", minimum_confidence=0.5))
