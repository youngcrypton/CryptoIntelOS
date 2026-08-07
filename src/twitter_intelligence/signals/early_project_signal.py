from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule

class EarlyProjectSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Early Project", ("Active Founder", "Product Shipping"), ("Founder Credibility", "Product Maturity"), "medium", "Add the project to early-stage monitoring."))
