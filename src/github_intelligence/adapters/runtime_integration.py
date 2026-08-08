from dataclasses import dataclass

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation, Signal
from src.github_intelligence.analysis.repository_analyzer import RepositoryAnalysis
from src.github_intelligence.models import Repository
from src.github_intelligence.organization_analyzer import OrganizationIntelligence
from src.github_intelligence.repository_scoring import RepositoryScore
from src.github_intelligence.signal_engine import GitHubIntelligenceSignal
from src.platform_sdk import execute_synchronously
from src.runtime.engine import ExecutionContext, ExecutionResult
from src.runtime.synchronous import SynchronousRuntime, SynchronousRuntimeResult

from .assessment_adapter import RepositoryAssessmentAdapter
from .evidence_adapter import GitHubEvidenceAdapter
from .finding_adapter import RepositoryFindingAdapter
from .observation_adapter import RepositoryObservationAdapter
from .signal_adapter import GitHubSignalAdapter


@dataclass(frozen=True, slots=True)
class GitHubRuntimeResult:
    observation: Observation
    evidence: tuple[Evidence, ...]
    finding: Finding
    assessment: Assessment
    signals: tuple[Signal, ...]
    runtime: SynchronousRuntimeResult

    @property
    def execution(self) -> ExecutionResult:
        """Deprecated compatibility view of the canonical Runtime result."""

        return self.runtime.execution


class GitHubRuntimeIntegration:
    """Synchronous composition boundary for the first GitHub Runtime slice."""

    def __init__(self, runtime: SynchronousRuntime | None = None) -> None:
        self.runtime = runtime or SynchronousRuntime()
        self.observations = RepositoryObservationAdapter()
        self.evidence = GitHubEvidenceAdapter()
        self.findings = RepositoryFindingAdapter()
        self.assessments = RepositoryAssessmentAdapter()
        self.signals = GitHubSignalAdapter()

    def process(
        self,
        repository: Repository,
        analysis: RepositoryAnalysis,
        score: RepositoryScore,
        signals: tuple[GitHubIntelligenceSignal, ...] = (),
        organization: OrganizationIntelligence | None = None,
    ) -> GitHubRuntimeResult:
        observation = self.observations.to_observation(repository)
        entity_reference = f"github:repository:{repository.id}"
        evidence_items = [self.evidence.repository(repository, entity_reference=entity_reference)]
        evidence_items.extend(
            self.evidence.contributor(item, entity_reference=entity_reference)
            for item in analysis.contributor_intelligence
        )
        if organization is not None:
            evidence_items.append(
                self.evidence.organization(
                    organization, entity_reference=entity_reference
                )
            )
        evidence = tuple(evidence_items)
        finding = self.findings.to_finding(
            analysis, evidence=tuple(item.evidence_id for item in evidence)
        )
        assessment = self.assessments.to_assessment(
            score,
            evidence=(finding.finding_id,),
            entity_reference=entity_reference,
        )
        canonical_signals = tuple(
            self.signals.to_signal(item, entity_reference=entity_reference)
            for item in signals
        )
        runtime = execute_synchronously(
            self.runtime,
            (observation, evidence, (finding,), (assessment,), canonical_signals),
            ExecutionContext(
                f"github:{repository.id}", "1.0", observation.observed_at
            ),
        )
        return GitHubRuntimeResult(
            observation,
            evidence,
            finding,
            assessment,
            canonical_signals,
            runtime,
        )
