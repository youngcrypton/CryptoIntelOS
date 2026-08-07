from src.core_intelligence.models import Signal
from src.website_intelligence.analysis import AnalysisOutput

from .signal_builder import SignalBuilder, SignalRule


class ConfiguredSignalGenerator:
    def __init__(self, rule: SignalRule) -> None:
        self.rule = rule
        self.signal_type = rule.signal_type
        self._builder = SignalBuilder()

    def generate(self, output: AnalysisOutput) -> Signal | None:
        return self._builder.build(output, self.rule)
