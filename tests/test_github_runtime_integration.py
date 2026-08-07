from datetime import UTC, datetime
from types import SimpleNamespace

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation, Signal
from src.github_intelligence.adapters import GitHubRuntimeIntegration
from src.github_intelligence.analysis.repository_analyzer import RepositoryAnalysis
from src.github_intelligence.models import Repository
from src.github_intelligence.organization_analyzer import OrganizationIntelligence
from src.github_intelligence.signal_engine import GitHubIntelligenceSignal
from src.runtime.engine import ExecutionState


def test_github_outputs_cross_runtime_boundary_as_canonical_objects() -> None:
    repository = Repository(1, "crypto", "acme/crypto", updated_at="2026-01-01T00:00:00Z")
    analysis = RepositoryAnalysis(repository, ["Python"], {"commits": 4}, {"license": "MIT"})
    score = SimpleNamespace(overall_repository_score=82.0, confidence_score=91.0)
    organization = OrganizationIntelligence(
        id=7,
        login="acme",
        name="Acme",
        verified=True,
        repository_count=12,
        public_member_count=4,
        followers=100,
        following=2,
        description=None,
        website=None,
        location=None,
        created_at=None,
        updated_at=None,
        html_url=None,
        avatar_url=None,
        email=None,
        twitter_username=None,
    )
    github_signal = GitHubIntelligenceSignal(
        signal_id="ACTIVE_DEVELOPMENT",
        signal_name="Active Development",
        category="development",
        severity="high",
        confidence=0.91,
        supporting_evidence=("recent commits",),
        contributing_metrics={"commits": 4},
        explanation="Recent commits demonstrate active development.",
        timestamp=datetime.now(UTC),
        source_analyzers=("CommitAnalyzer",),
        repository_score_components={"development_activity": 82.0},
    )

    result = GitHubRuntimeIntegration().process(
        repository,
        analysis,
        score,
        (github_signal,),
        organization,
    )

    assert isinstance(result.observation, Observation)
    assert isinstance(result.evidence[0], Evidence)
    assert isinstance(result.finding, Finding)
    assert isinstance(result.assessment, Assessment)
    assert isinstance(result.signals[0], Signal)
    assert result.execution.final_state is ExecutionState.COMPLETED
    assert result.execution.completed_stages[-1] == "distribute"
