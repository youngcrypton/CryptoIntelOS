from datetime import UTC, datetime

from src.platform_sdk import RuntimeFacade
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.twitter_intelligence import (
    TwitterAnalysisEngine,
    TwitterDiscoveryEngine,
    TwitterPost,
    TwitterRuntimeIntegration,
)


NOW = datetime(2026, 8, 7, tzinfo=UTC)


def analyze(text: str):
    observation = TwitterDiscoveryEngine().discover_post(
        TwitterPost("post-1", "project-1", text, NOW)
    ).observation
    return TwitterAnalysisEngine().analyze(observation)


def finding_types(output) -> set[str]:
    return {finding.finding_type for finding in output.findings}


def assessment_types(output) -> set[str]:
    return {assessment.assessment_type for assessment in output.assessments}


def test_founder_analysis() -> None:
    output = analyze("Our founder and CEO shared the roadmap")
    assert "twitter.founder" in {item.metric for item in output.evidence}
    assert "Active Founder" in finding_types(output)
    assert "Founder Credibility" in assessment_types(output)


def test_hiring_analysis() -> None:
    output = analyze("We're hiring. Join our team")
    assert "Hiring Activity" in finding_types(output)
    assert "Team Visibility" in assessment_types(output)


def test_funding_analysis() -> None:
    output = analyze("We raised a seed round of funding")
    assert "Funding Activity" in finding_types(output)
    assert "Funding Confidence" in assessment_types(output)


def test_partnership_analysis() -> None:
    output = analyze("New partnership and integration announced")
    assert "Partnership Activity" in finding_types(output)
    assert "Partnership Confidence" in assessment_types(output)


def test_ecosystem_analysis() -> None:
    output = analyze("Expanding across the DeFi ecosystem")
    assert "Ecosystem Expansion" in finding_types(output)
    assert "Ecosystem Presence" in assessment_types(output)


def test_narrative_analysis() -> None:
    output = analyze("AI and RWA are emerging narratives")
    assert "Emerging Narrative" in finding_types(output)
    assert "Narrative Strength" in assessment_types(output)


def test_community_analysis() -> None:
    output = analyze("Community AMA for all users in Discord")
    assert "Strong Community" in finding_types(output)
    assert "Community Health" in assessment_types(output)


def test_assessment_generation_is_deterministic() -> None:
    first = analyze("Founder launch partnership in the DeFi ecosystem")
    second = analyze("Founder launch partnership in the DeFi ecosystem")
    assert first.evidence == second.evidence
    assert first.findings == second.findings
    assert first.assessments == second.assessments
    assert all(0 <= item.score <= 100 for item in first.assessments)


def test_runtime_delegation_excludes_signals() -> None:
    output = analyze("Founder launch with our community")
    received = []

    def runtime_entrypoint(canonical_output, context):
        received.append(canonical_output)
        return ExecutionResult(context.execution_id, ExecutionState.COMPLETED)

    context = ExecutionContext("execution-1", "1.0", NOW)
    result = TwitterAnalysisEngine.enter_runtime(
        output, TwitterRuntimeIntegration(RuntimeFacade(runtime_entrypoint)), context
    )
    assert result.final_state is ExecutionState.COMPLETED
    assert received[0][0] == output.observation
    assert received[0][1:4] == (output.evidence, output.findings, output.assessments)
    assert received[0][4] == ()
