from typing import Protocol

from src.core_intelligence.models import Signal
from src.website_intelligence.analysis import AnalysisOutput

from .exceptions import DuplicateSignalGeneratorError


class SignalGenerator(Protocol):
    signal_type: str

    def generate(self, output: AnalysisOutput) -> Signal | None: ...


class SignalRegistry:
    """Ordered registry of Website signal generators."""

    def __init__(self) -> None:
        self._generators: dict[str, SignalGenerator] = {}

    def register(self, generator: SignalGenerator) -> None:
        if generator.signal_type in self._generators:
            raise DuplicateSignalGeneratorError(generator.signal_type)
        self._generators[generator.signal_type] = generator

    def generators(self) -> tuple[SignalGenerator, ...]:
        return tuple(self._generators.values())
