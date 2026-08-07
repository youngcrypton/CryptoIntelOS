from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule


class RoadmapSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Roadmap Visibility", ("Public Roadmap",), ("Documentation Quality",), "medium", "Monitor roadmap delivery against published milestones."))
