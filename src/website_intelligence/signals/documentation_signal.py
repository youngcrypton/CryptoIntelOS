from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule


class DocumentationSignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Documentation Strength", ("Strong Documentation",), ("Documentation Quality",), "medium", "Review documentation depth and verify referenced claims."))
