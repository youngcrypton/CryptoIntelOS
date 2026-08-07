from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule

class NarrativeSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Narrative Acceleration", ("Emerging Narrative",), ("Narrative Strength",), "medium", "Track narrative traction across the ecosystem."))
