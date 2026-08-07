from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule

class PartnershipSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Partnership Confirmed", ("Partnership Activity",), ("Partnership Confidence",), "medium", "Validate the partnership scope and integration status."))
