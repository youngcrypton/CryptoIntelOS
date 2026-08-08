import sys
from dataclasses import dataclass
from typing import TextIO

from src.core_intelligence.models import Observation
from src.platform_sdk import RuntimeFacade, execute_synchronously
from src.platform_sdk.runtime import CanonicalOutput
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.runtime.synchronous import SynchronousRuntime, SynchronousRuntimeResult

from .analysis import AnalysisOutput, TwitterAnalysisEngine
from .discovery import DiscoveryResult, TwitterDiscoveryEngine
from .models import TwitterPost, TwitterProfile
from .runtime import TwitterRuntimeIntegration
from .signals import SignalOutput, TwitterSignalEngine


@dataclass(frozen=True, slots=True)
class TwitterVerticalSliceResult:
    discoveries: tuple[DiscoveryResult, ...]
    canonical: SignalOutput
    runtime: SynchronousRuntimeResult
    console_summary: str


class TwitterVerticalSlice:
    """Run Twitter profile and post content through the complete platform."""

    def __init__(
        self,
        *,
        discovery: TwitterDiscoveryEngine | None = None,
        analysis: TwitterAnalysisEngine | None = None,
        signals: TwitterSignalEngine | None = None,
        runtime: SynchronousRuntime | None = None,
    ) -> None:
        self.discovery = discovery or TwitterDiscoveryEngine()
        self.analysis = analysis or TwitterAnalysisEngine()
        self.signals = signals or TwitterSignalEngine()
        self.runtime = runtime or SynchronousRuntime()

    def run(
        self,
        profile: TwitterProfile,
        posts: tuple[TwitterPost, ...],
        *,
        output: TextIO | None = None,
    ) -> TwitterVerticalSliceResult:
        if not posts:
            raise ValueError("at least one Twitter post is required")
        discoveries = (
            self.discovery.discover_profile(profile),
            *(self.discovery.discover_post(post) for post in posts),
        )
        batch_observation = self._batch_observation(discoveries)
        analyses = tuple(self.analysis.analyze(result.observation) for result in discoveries)
        combined_analysis = AnalysisOutput(
            batch_observation,
            tuple(item for analysis in analyses for item in analysis.evidence),
            tuple(item for analysis in analyses for item in analysis.findings),
            tuple(item for analysis in analyses for item in analysis.assessments),
        )
        generated = tuple(self.signals.generate(analysis) for analysis in analyses)
        canonical = SignalOutput(
            combined_analysis.observation,
            combined_analysis.evidence,
            combined_analysis.findings,
            combined_analysis.assessments,
            tuple(signal for result in generated for signal in result.signals),
        )
        runtime = self._execute_runtime(canonical, profile.user_id)
        summary = self._summary(profile, posts, discoveries, canonical, runtime)
        print(summary, file=output or sys.stdout)
        return TwitterVerticalSliceResult(discoveries, canonical, runtime, summary)

    def _batch_observation(
        self, discoveries: tuple[DiscoveryResult, ...]
    ) -> Observation:
        captured: list[CanonicalOutput] = []

        def capture(
            canonical_output: CanonicalOutput, context: ExecutionContext
        ) -> ExecutionResult:
            captured.append(canonical_output)
            return ExecutionResult(context.execution_id, ExecutionState.COMPLETED)

        context = ExecutionContext(
            f"twitter:discovery:{discoveries[0].observation.source_identifier}",
            "1.0",
            discoveries[0].observation.collected_at,
        )
        self.discovery.enter_runtime(
            discoveries,
            TwitterRuntimeIntegration(RuntimeFacade(capture)),
            context,
        )
        return captured[0][0]

    def _execute_runtime(
        self, canonical: SignalOutput, user_id: str
    ) -> SynchronousRuntimeResult:
        captured: list[SynchronousRuntimeResult] = []

        def execute(
            canonical_output: CanonicalOutput, context: ExecutionContext
        ) -> ExecutionResult:
            result = execute_synchronously(self.runtime, canonical_output, context)
            captured.append(result)
            return result.execution

        context = ExecutionContext(
            f"twitter:{user_id}", "1.0", canonical.observation.observed_at
        )
        self.signals.enter_runtime(
            canonical,
            TwitterRuntimeIntegration(RuntimeFacade(execute)),
            context,
        )
        return captured[0]

    @staticmethod
    def _summary(
        profile: TwitterProfile,
        posts: tuple[TwitterPost, ...],
        discoveries: tuple[DiscoveryResult, ...],
        canonical: SignalOutput,
        runtime: SynchronousRuntimeResult,
    ) -> str:
        lines = (
            f"Twitter Profile Processed: @{profile.username}",
            f"Posts Discovered: {len(posts)}",
            f"Observations Created: {len(discoveries)}",
            f"Evidence Generated: {len(canonical.evidence)}",
            f"Findings Generated: {len(canonical.findings)}",
            f"Assessments Produced: {len(canonical.assessments)}",
            f"Signals Generated: {len(canonical.signals)}",
            f"Compiler Executed: {len(runtime.compilation.projection.nodes)} nodes",
            f"Knowledge Graph Updated: {len(runtime.graph.nodes)} nodes",
            f"Correlation Completed: {runtime.correlation.status.value}",
            f"Reasoning Completed: {runtime.reasoning.status.value}",
            f"Automation Plan Created: {len(runtime.automation.actions)} actions",
            f"Distribution Plan Created: {len(runtime.distribution.requests)} requests",
            f"Execution Successful: {runtime.execution.final_state.value}",
        )
        return "\n".join(lines)
