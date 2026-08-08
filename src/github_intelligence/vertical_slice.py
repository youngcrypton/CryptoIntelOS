from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, TextIO
import sys
from datetime import UTC, datetime

from src.platform_sdk import execute_synchronously
from src.runtime.engine import ExecutionContext
from src.runtime.synchronous import SynchronousRuntime, SynchronousRuntimeResult

from .adapters import GitHubRuntimeIntegration, GitHubRuntimeResult
from .analysis.repository_analyzer import RepositoryAnalyzer
from .models import Repository
from .organization_analyzer import OrganizationIntelligence
from .repository_scoring import RepositoryScoringEngine
from .signal_engine import GitHubSignalEngine


@dataclass(frozen=True, slots=True)
class GitHubVerticalSliceResult:
    canonical: GitHubRuntimeResult
    runtime: SynchronousRuntimeResult
    console_summary: str


class GitHubVerticalSlice:
    """Run one GitHub repository through the complete synchronous platform."""

    def __init__(
        self,
        *,
        repository_analyzer: RepositoryAnalyzer | None = None,
        scoring_engine: RepositoryScoringEngine | None = None,
        signal_engine: GitHubSignalEngine | None = None,
        adapters: GitHubRuntimeIntegration | None = None,
        runtime: SynchronousRuntime | None = None,
    ) -> None:
        self.repository_analyzer = repository_analyzer or RepositoryAnalyzer()
        self.scoring_engine = scoring_engine or RepositoryScoringEngine()
        self.signal_engine = signal_engine or GitHubSignalEngine()
        self.adapters = adapters or GitHubRuntimeIntegration()
        self.runtime = runtime or SynchronousRuntime()

    def run(
        self,
        repository: Repository,
        metadata: Mapping[str, Any] | None = None,
        *,
        organization: OrganizationIntelligence | None = None,
        output: TextIO | None = None,
    ) -> GitHubVerticalSliceResult:
        analysis = self.repository_analyzer.analyze(repository, metadata)
        score = self.scoring_engine.score(analysis)
        github_signals = tuple(self.signal_engine.generate(analysis, score))
        canonical = self.adapters.process(
            repository,
            analysis,
            score,
            github_signals,
            organization,
        )
        output_projection = (
            canonical.observation,
            canonical.evidence,
            (canonical.finding,),
            (canonical.assessment,),
            canonical.signals,
        )
        context = ExecutionContext(
            f"github:{repository.id}", "1.0", datetime.now(UTC)
        )
        runtime = execute_synchronously(self.runtime, output_projection, context)
        summary = self._summary(repository, canonical, runtime)
        print(summary, file=output or sys.stdout)
        return GitHubVerticalSliceResult(canonical, runtime, summary)

    @staticmethod
    def _summary(
        repository: Repository,
        canonical: GitHubRuntimeResult,
        runtime: SynchronousRuntimeResult,
    ) -> str:
        lines = (
            f"Repository: {repository.full_name}",
            f"Observation Created: {canonical.observation.observation_id}",
            f"Evidence Extracted: {len(canonical.evidence)}",
            f"Finding Generated: {canonical.finding.finding_id}",
            f"Assessment Produced: {canonical.assessment.score:.2f}",
            f"Signals Generated: {len(canonical.signals)}",
            f"Compiler Executed: {len(runtime.compilation.projection.nodes)} nodes",
            f"Knowledge Graph Updated: {len(runtime.graph.nodes)} nodes",
            f"Correlation Completed: {runtime.correlation.status.value}",
            f"Reasoning Completed: {runtime.reasoning.status.value}",
            f"Automation Plan Created: {runtime.automation.plan_id}",
            f"Distribution Plan Created: {runtime.distribution.plan_id}",
            f"Execution Successful: {runtime.execution.final_state.value}",
        )
        return "\n".join(lines)
