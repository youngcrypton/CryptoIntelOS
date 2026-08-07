from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule

class LaunchSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Product Launch Imminent", ("Product Shipping",), ("Product Maturity",), "high", "Monitor launch timing, availability, and adoption."))
