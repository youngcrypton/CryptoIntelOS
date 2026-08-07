from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule


class IdentitySignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Official Website Verified", ("Verified Official Website",), ("Identity Confidence",), "medium", "Use the website as the authoritative project identity anchor."))
