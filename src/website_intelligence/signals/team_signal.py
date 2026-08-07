from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule


class TeamSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Team Transparency", ("Transparent Team",), ("Team Transparency",), "medium", "Verify public team identities and relevant experience."))
