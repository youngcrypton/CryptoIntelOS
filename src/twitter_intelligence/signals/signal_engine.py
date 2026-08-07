from dataclasses import dataclass

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation, Signal
from src.runtime.engine import ExecutionContext, ExecutionResult
from src.twitter_intelligence.analysis import AnalysisOutput

from ..runtime import TwitterRuntimeIntegration
from .early_project_signal import EarlyProjectSignal
from .ecosystem_signal import EcosystemSignal
from .founder_signal import FounderSignal
from .funding_signal import FundingSignal
from .hidden_gem_signal import HiddenGemSignal
from .hiring_signal import HiringSignal
from .launch_signal import LaunchSignal
from .narrative_signal import NarrativeSignal
from .partnership_signal import PartnershipSignal
from .signal_registry import SignalRegistry
from .watchlist_signal import WatchlistSignal


@dataclass(frozen=True, slots=True)
class SignalOutput:
    observation: Observation
    evidence: tuple[Evidence, ...]
    findings: tuple[Finding, ...]
    assessments: tuple[Assessment, ...]
    signals: tuple[Signal, ...]


class TwitterSignalEngine:
    """Generate registered canonical signals from Twitter analysis output."""

    def __init__(self, registry: SignalRegistry | None = None) -> None:
        self.registry = registry or self.default_registry()

    @staticmethod
    def default_registry() -> SignalRegistry:
        registry = SignalRegistry()
        for generator in (
            HiddenGemSignal(), EarlyProjectSignal(), FounderSignal(), HiringSignal(),
            FundingSignal(), PartnershipSignal(), EcosystemSignal(), NarrativeSignal(),
            LaunchSignal(), WatchlistSignal(),
        ):
            registry.register(generator)
        return registry

    def generate(self, output: AnalysisOutput) -> SignalOutput:
        signals = tuple(
            signal
            for generator in self.registry.generators()
            if (signal := generator.generate(output)) is not None
        )
        return SignalOutput(
            output.observation, output.evidence, output.findings, output.assessments, signals
        )

    @staticmethod
    def enter_runtime(
        output: SignalOutput,
        integration: TwitterRuntimeIntegration,
        context: ExecutionContext,
    ) -> ExecutionResult:
        return integration.integrate(
            (output.observation, output.evidence, output.findings, output.assessments, output.signals),
            context,
        )
