from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule


class CommunicationSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Communication Strength", ("Strong Communication",), ("Communication Quality",), "medium", "Monitor official communication channels for material updates."))
