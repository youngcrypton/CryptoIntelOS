from io import StringIO

from src.github_intelligence.models import Repository
from src.github_intelligence.vertical_slice import GitHubVerticalSlice
from src.runtime.automation import AutomationPlan
from src.runtime.correlation import CorrelationStatus
from src.runtime.distribution import DistributionPlan, DistributionStatus
from src.runtime.engine import ExecutionState
from src.runtime.reasoning import ReasoningStatus


def test_github_executes_complete_synchronous_vertical_slice() -> None:
    repository = Repository(
        id=42,
        name="cryptointel",
        full_name="acme/cryptointel",
        description="Crypto intelligence platform",
        default_branch="main",
        updated_at="2026-08-07T12:00:00Z",
    )
    output = StringIO()

    result = GitHubVerticalSlice().run(
        repository,
        {
            "description": repository.description,
            "default_branch": "main",
            "license": "MIT",
            "topics": ["crypto", "intelligence"],
            "language": "Python",
        },
        output=output,
    )

    assert result.canonical.observation.source == "github"
    assert result.canonical.evidence
    assert result.canonical.finding.supporting_evidence
    assert result.canonical.assessment.evidence
    assert result.canonical.signals
    assert result.runtime.compilation.projection.nodes
    assert len(result.runtime.graph.nodes) == len(result.runtime.compilation.projection.nodes)
    assert result.runtime.correlation.status is CorrelationStatus.CONFIRMED
    assert result.runtime.reasoning.status is ReasoningStatus.COMPLETED
    assert isinstance(result.runtime.automation, AutomationPlan)
    assert isinstance(result.runtime.distribution, DistributionPlan)
    assert result.runtime.distribution_results[0].status is DistributionStatus.ACCEPTED
    assert result.runtime.execution.final_state is ExecutionState.COMPLETED
    assert "Execution Successful: completed" in output.getvalue()
