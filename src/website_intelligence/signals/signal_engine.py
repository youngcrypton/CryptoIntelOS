from dataclasses import dataclass

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation, Signal
from src.runtime.engine import ExecutionContext, ExecutionResult
from src.website_intelligence.analysis import AnalysisOutput

from ..runtime import WebsiteRuntimeIntegration
from .signal_registry import SignalRegistry
from .communication_signal import CommunicationSignal
from .documentation_signal import DocumentationSignal
from .dormant_signal import DormantSignal
from .ecosystem_signal import EcosystemSignal
from .hiring_signal import HiringSignal
from .identity_signal import IdentitySignal
from .roadmap_signal import RoadmapSignal
from .security_signal import SecuritySignal
from .team_signal import TeamSignal


@dataclass(frozen=True, slots=True)
class SignalOutput:
    observation: Observation
    evidence: tuple[Evidence, ...]
    findings: tuple[Finding, ...]
    assessments: tuple[Assessment, ...]
    signals: tuple[Signal, ...]


class WebsiteSignalEngine:
    """Generate deterministic Website signals from analysis output."""

    def __init__(self, registry: SignalRegistry | None = None) -> None:
        self.registry = registry or self.default_registry()

    @classmethod
    def default_registry(cls) -> SignalRegistry:
        registry = SignalRegistry()
        for generator in (IdentitySignal(), DocumentationSignal(), RoadmapSignal(), TeamSignal(), HiringSignal(), SecuritySignal(), EcosystemSignal(), CommunicationSignal(), DormantSignal()):
            registry.register(generator)
        return registry

    def generate(self, output: AnalysisOutput) -> SignalOutput:
        signals = tuple(signal for generator in self.registry.generators() if (signal := generator.generate(output)) is not None)
        return SignalOutput(output.observation, output.evidence, output.findings, output.assessments, signals)

    @staticmethod
    def enter_runtime(output: SignalOutput, integration: WebsiteRuntimeIntegration, context: ExecutionContext) -> ExecutionResult:
        return integration.integrate((output.observation, output.evidence, output.findings, output.assessments, output.signals), context)
