"""Focused tests for the explainable GitHub intelligence signal engine."""

from datetime import datetime, timezone

from src.github_intelligence import (
    GitHubSignalEngine,
    GitHubSignalRule,
    RepositoryScore,
    ScoreExplanation,
    SignalRuleMatch,
)
from src.github_intelligence.analysis.repository_analyzer import RepositoryAnalysis
from src.github_intelligence.models import Repository


def explanation(score: float = 70.0, confidence: float = 80.0) -> ScoreExplanation:
    return ScoreExplanation(
        score=score,
        contributing_factors=("test factor",),
        penalties=(),
        bonuses=(),
        confidence=confidence,
        evidence_sources=("test analyzer",),
    )


def repository_score() -> RepositoryScore:
    value = explanation()
    return RepositoryScore(
        repository_quality_score=value,
        organization_quality_score=value,
        contributor_quality_score=value,
        development_activity_score=value,
        release_quality_score=value,
        dependency_health_score=value,
        supply_chain_risk_score=explanation(10.0),
        documentation_score=value,
        security_score=explanation(50.0, 0.0),
        governance_score=explanation(50.0, 0.0),
        overall_repository_score=72.0,
        confidence_score=76.0,
        repository_tier="Tier B",
        risk_classification="Promising",
        weights={},
    )


def repository() -> RepositoryAnalysis:
    return RepositoryAnalysis(
        repository=Repository(id=1, name="project", full_name="crypto/project"),
        technologies=["Python"],
        activity_metrics={},
        metadata={"description": "Developer tooling", "topics": ["sdk"]},
    )


def custom_rule() -> GitHubSignalRule:
    return GitHubSignalRule(
        signal_id="TEST_SIGNAL",
        signal_name="Test Signal",
        category="test",
        source_analyzers=("RepositoryAnalyzer", "RepositoryScoringEngine"),
        evaluator=lambda context: SignalRuleMatch(
            supporting_evidence=("repository score exceeds test threshold",),
            contributing_metrics={"overall_score": context.repository_score.overall_repository_score},
            explanation="A transparent test rule matched the supplied repository score.",
            score_components=("repository_quality",),
            evidence_strength=90.0,
        ),
    )


def test_signal_generation_uses_registered_rules() -> None:
    engine = GitHubSignalEngine(rules=[custom_rule()])

    signals = engine.generate(
        repository(), repository_score(), timestamp=datetime(2026, 8, 6, tzinfo=timezone.utc)
    )

    assert len(signals) == 1
    assert signals[0].signal_id == "TEST_SIGNAL"
    assert signals[0].signal_name == "Test Signal"


def test_confidence_calculation_correlates_score_and_rule_evidence() -> None:
    confidence = GitHubSignalEngine.calculate_confidence(
        repository_score(), ("repository_quality",), 90.0
    )

    assert confidence == 83.0


def test_evidence_aggregation_references_repository_components() -> None:
    evidence = GitHubSignalEngine.aggregate_score_evidence(
        repository_score(), ("repository_quality", "development_activity")
    )

    assert evidence == {
        "repository_quality": 70.0,
        "development_activity": 70.0,
        "overall_repository_score": 72.0,
    }


def test_severity_classification_handles_positive_and_risk_signals() -> None:
    assert GitHubSignalEngine.classify_severity(90.0) == "high"
    assert GitHubSignalEngine.classify_severity(90.0, risk_signal=True) == "critical"
    assert GitHubSignalEngine.classify_severity(50.0, risk_signal=True) == "medium"


def test_generated_signal_is_fully_explainable() -> None:
    signal = GitHubSignalEngine(rules=[custom_rule()]).generate(
        repository(), repository_score()
    )[0]

    assert signal.supporting_evidence
    assert signal.contributing_metrics["overall_score"] == 72.0
    assert signal.explanation
    assert signal.source_analyzers == (
        "RepositoryAnalyzer",
        "RepositoryScoringEngine",
    )
    assert signal.repository_score_components["repository_quality"] == 70.0
