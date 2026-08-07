from datetime import UTC, datetime
from io import StringIO

from src.runtime.correlation import CorrelationStatus
from src.runtime.distribution import DistributionStatus
from src.runtime.engine import ExecutionState
from src.runtime.reasoning import ReasoningStatus
from src.twitter_intelligence import (
    TwitterPost,
    TwitterProfile,
    TwitterVerticalSlice,
)


def test_twitter_end_to_end_vertical_slice() -> None:
    timestamp = datetime(2026, 8, 7, tzinfo=UTC)
    profile = TwitterProfile(
        "project-1", "cryptoproject", "Crypto Project", "Official DeFi protocol"
    )
    posts = (
        TwitterPost(
            "post-1",
            profile.user_id,
            "Founder and CEO announced a product launch, DeFi ecosystem partnership, "
            "seed funding, community AMA, and we're hiring. Join our team.",
            timestamp,
        ),
    )
    console = StringIO()

    result = TwitterVerticalSlice().run(profile, posts, output=console)

    assert len(result.discoveries) == 2
    assert result.discoveries[0].discovery_type == "profile"
    assert result.discoveries[1].discovery_type == "post"
    assert result.canonical.observation.source == "twitter"
    assert result.canonical.evidence
    assert result.canonical.findings
    assert result.canonical.assessments
    assert result.canonical.signals
    expected_nodes = (
        1
        + len(result.canonical.evidence)
        + len(result.canonical.findings)
        + len(result.canonical.assessments)
        + len(result.canonical.signals)
    )
    assert len(result.runtime.compilation.projection.nodes) == expected_nodes
    assert len(result.runtime.graph.nodes) == expected_nodes
    assert result.runtime.correlation.status is CorrelationStatus.CONFIRMED
    assert result.runtime.reasoning.status is ReasoningStatus.COMPLETED
    assert result.runtime.automation.actions
    assert result.runtime.distribution.requests
    assert result.runtime.distribution_results[0].status is DistributionStatus.ACCEPTED
    assert result.runtime.execution.final_state is ExecutionState.COMPLETED
    summary = console.getvalue()
    for phrase in (
        "Twitter Profile Processed",
        "Posts Discovered",
        "Observations Created",
        "Evidence Generated",
        "Findings Generated",
        "Assessments Produced",
        "Signals Generated",
        "Compiler Executed",
        "Knowledge Graph Updated",
        "Correlation Completed",
        "Reasoning Completed",
        "Automation Plan Created",
        "Distribution Plan Created",
        "Execution Successful",
    ):
        assert phrase in summary
