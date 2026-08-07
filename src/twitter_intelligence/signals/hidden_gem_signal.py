from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule

class HiddenGemSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Hidden Gem Candidate", ("Product Shipping", "Ecosystem Expansion", "Emerging Narrative"), ("Product Maturity", "Ecosystem Presence"), "medium", "Monitor the project for sustained execution."))
