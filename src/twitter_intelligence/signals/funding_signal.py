from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule

class FundingSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Funding Detected", ("Funding Activity",), ("Funding Confidence",), "high", "Verify the funding announcement and monitor execution."))
