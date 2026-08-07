from ._configured import ConfiguredSignalGenerator
from .signal_builder import SignalRule


class SecuritySignal(ConfiguredSignalGenerator):
    def __init__(self) -> None:
        super().__init__(SignalRule("Security Readiness", ("Security Focus",), ("Security Maturity",), "high", "Verify audits and monitor security disclosures."))
