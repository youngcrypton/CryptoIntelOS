"""Focused tests for the explainable GitHub repository scoring engine."""

from src.github_intelligence import RepositoryScoringEngine
from src.github_intelligence.analysis.repository_analyzer import RepositoryAnalysis
from src.github_intelligence.models import Repository


def repository_analysis() -> RepositoryAnalysis:
    return RepositoryAnalysis(
        repository=Repository(
            id=1,
            name="project",
            full_name="crypto/project",
            description="A project",
            default_branch="main",
        ),
        technologies=["Python", "Solidity"],
        activity_metrics={},
        metadata={
            "description": "A project",
            "homepage": "https://project.example",
            "topics": ["crypto"],
            "license": "MIT",
            "default_branch": "main",
        },
    )


def neutral_scores(value: float) -> dict[str, float]:
    return {
        category: value for category in RepositoryScoringEngine.DEFAULT_WEIGHTS
    }


def test_weighting_respects_configured_category_importance() -> None:
    engine = RepositoryScoringEngine(
        {
            "repository_quality": 1.0,
            **{
                category: 0.0
                for category in RepositoryScoringEngine.DEFAULT_WEIGHTS
                if category != "repository_quality"
            },
        }
    )
    scores = neutral_scores(0.0)
    scores["repository_quality"] = 82.0

    assert engine.calculate_weighted_score(scores) == 82.0


def test_score_calculation_uses_repository_evidence() -> None:
    score = RepositoryScoringEngine().score(repository_analysis())

    assert score.repository_quality_score.score == 91.0
    assert score.documentation_score.score == 100.0
    assert 0.0 <= score.overall_repository_score <= 100.0


def test_tier_assignment() -> None:
    expected_tiers = {
        95: "Tier S",
        85: "Tier A",
        70: "Tier B",
        55: "Tier C",
        30: "Tier D",
    }

    assert {
        score: RepositoryScoringEngine.assign_tier(score)
        for score in expected_tiers
    } == expected_tiers


def test_every_category_is_explainable() -> None:
    score = RepositoryScoringEngine().score(repository_analysis())
    explanations = (
        score.repository_quality_score,
        score.organization_quality_score,
        score.contributor_quality_score,
        score.development_activity_score,
        score.release_quality_score,
        score.dependency_health_score,
        score.supply_chain_risk_score,
        score.documentation_score,
        score.security_score,
        score.governance_score,
    )

    assert all(explanation.contributing_factors for explanation in explanations)
    assert all(explanation.evidence_sources for explanation in explanations)
    assert all(0 <= explanation.confidence <= 100 for explanation in explanations)


def test_confidence_calculation_uses_category_weights() -> None:
    engine = RepositoryScoringEngine()
    confidences = neutral_scores(100.0)
    confidences["security"] = 0.0
    confidences["governance"] = 0.0

    assert engine.calculate_confidence(confidences) == 95.0
