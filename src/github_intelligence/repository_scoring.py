"""Transparent weighted scoring for existing GitHub intelligence models."""

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from statistics import mean
from typing import TYPE_CHECKING

from .analysis.repository_analyzer import RepositoryAnalysis
from .commit_analyzer import CommitIntelligence
from .contributor_analyzer import ContributorIntelligence
from .dependency_analyzer import DependencyIntelligence
from .release_analyzer import ReleaseIntelligence

if TYPE_CHECKING:
    from .organization_analyzer import OrganizationIntelligence


@dataclass(frozen=True)
class ScoreExplanation:
    """Explain one category score using explicit evidence and adjustments."""

    score: float
    contributing_factors: tuple[str, ...]
    penalties: tuple[str, ...]
    bonuses: tuple[str, ...]
    confidence: float
    evidence_sources: tuple[str, ...]


@dataclass(frozen=True)
class RepositoryScore:
    """Complete explainable repository score across all Phase 2 categories."""

    repository_quality_score: ScoreExplanation
    organization_quality_score: ScoreExplanation
    contributor_quality_score: ScoreExplanation
    development_activity_score: ScoreExplanation
    release_quality_score: ScoreExplanation
    dependency_health_score: ScoreExplanation
    supply_chain_risk_score: ScoreExplanation
    documentation_score: ScoreExplanation
    security_score: ScoreExplanation
    governance_score: ScoreExplanation
    overall_repository_score: float
    confidence_score: float
    repository_tier: str
    risk_classification: str
    weights: dict[str, float]


class RepositoryScoringEngine:
    """Score existing intelligence deterministically without collecting new data.

    Default weights total 100 percent:

    - Repository quality: 15% -- baseline metadata and technical completeness.
    - Organization quality: 10% -- owner legitimacy and public presence.
    - Contributor quality: 15% -- diversity, activity, and bus-factor health.
    - Development activity: 20% -- the strongest signal of current execution.
    - Release quality: 15% -- delivery maturity, stability, and maintenance.
    - Dependency health: 10% -- freshness and ecosystem quality.
    - Supply-chain risk: 5% -- exposed as risk, inverted for overall quality.
    - Documentation: 5% -- available repository documentation indicators.
    - Security: 2.5% -- neutral placeholder until security intelligence exists.
    - Governance: 2.5% -- neutral placeholder until governance intelligence exists.
    """

    DEFAULT_WEIGHTS: dict[str, float] = {
        "repository_quality": 0.15,
        "organization_quality": 0.10,
        "contributor_quality": 0.15,
        "development_activity": 0.20,
        "release_quality": 0.15,
        "dependency_health": 0.10,
        "supply_chain_risk": 0.05,
        "documentation": 0.05,
        "security": 0.025,
        "governance": 0.025,
    }

    def __init__(self, weights: Mapping[str, float] | None = None) -> None:
        """Initialize with optional category-weight overrides."""

        configured = dict(self.DEFAULT_WEIGHTS)
        if weights:
            unknown = set(weights) - set(configured)
            if unknown:
                raise ValueError(f"unknown scoring categories: {sorted(unknown)}")
            configured.update(weights)
        if any(value < 0 for value in configured.values()):
            raise ValueError("scoring weights must not be negative")
        if sum(configured.values()) <= 0:
            raise ValueError("at least one scoring weight must be positive")
        self.weights = configured

    def score(
        self,
        repository: RepositoryAnalysis,
        organization: "OrganizationIntelligence | None" = None,
        contributors: Iterable[ContributorIntelligence] | None = None,
        commits: CommitIntelligence | None = None,
        releases: ReleaseIntelligence | None = None,
        dependencies: DependencyIntelligence | None = None,
        documentation_score: float | None = None,
    ) -> RepositoryScore:
        """Produce a complete score from already-collected intelligence models."""

        contributor_values = list(
            contributors
            if contributors is not None
            else repository.contributor_intelligence
        )
        commit_value = commits or repository.commit_intelligence
        release_value = releases or repository.release_intelligence
        dependency_value = dependencies or repository.dependency_intelligence

        categories = {
            "repository_quality": self._repository_quality(repository),
            "organization_quality": self._organization_quality(organization),
            "contributor_quality": self._contributor_quality(contributor_values),
            "development_activity": self._development_activity(commit_value),
            "release_quality": self._release_quality(release_value),
            "dependency_health": self._dependency_health(dependency_value),
            "supply_chain_risk": self._supply_chain_risk(dependency_value),
            "documentation": self._documentation(
                repository, documentation_score
            ),
            "security": self._placeholder("security intelligence"),
            "governance": self._placeholder("governance intelligence"),
        }
        weighted_scores = {name: value.score for name, value in categories.items()}
        weighted_scores["supply_chain_risk"] = (
            100.0 - categories["supply_chain_risk"].score
        )
        overall = self.calculate_weighted_score(weighted_scores)
        confidence = self.calculate_confidence(
            {name: value.confidence for name, value in categories.items()}
        )
        classification = self.classify_risk(
            overall,
            confidence,
            commit_value,
            release_value,
            dependency_value,
        )
        return RepositoryScore(
            repository_quality_score=categories["repository_quality"],
            organization_quality_score=categories["organization_quality"],
            contributor_quality_score=categories["contributor_quality"],
            development_activity_score=categories["development_activity"],
            release_quality_score=categories["release_quality"],
            dependency_health_score=categories["dependency_health"],
            supply_chain_risk_score=categories["supply_chain_risk"],
            documentation_score=categories["documentation"],
            security_score=categories["security"],
            governance_score=categories["governance"],
            overall_repository_score=overall,
            confidence_score=confidence,
            repository_tier=self.assign_tier(overall),
            risk_classification=classification,
            weights=dict(self.weights),
        )

    def calculate_weighted_score(self, scores: Mapping[str, float]) -> float:
        """Calculate a normalized weighted score for supplied categories."""

        missing = set(self.weights) - set(scores)
        if missing:
            raise ValueError(f"missing category scores: {sorted(missing)}")
        weight_total = sum(self.weights.values())
        result = sum(
            self._clamp(scores[name]) * weight for name, weight in self.weights.items()
        ) / weight_total
        return round(result, 2)

    def calculate_confidence(self, confidences: Mapping[str, float]) -> float:
        """Calculate weighted confidence using the same documented category weights."""

        missing = set(self.weights) - set(confidences)
        if missing:
            raise ValueError(f"missing category confidence: {sorted(missing)}")
        weight_total = sum(self.weights.values())
        result = sum(
            self._clamp(confidences[name]) * weight
            for name, weight in self.weights.items()
        ) / weight_total
        return round(result, 2)

    @staticmethod
    def assign_tier(score: float) -> str:
        """Assign the documented S-to-D repository tier."""

        if score >= 90:
            return "Tier S"
        if score >= 80:
            return "Tier A"
        if score >= 65:
            return "Tier B"
        if score >= 50:
            return "Tier C"
        return "Tier D"

    @staticmethod
    def classify_risk(
        overall: float,
        confidence: float,
        commits: CommitIntelligence | None,
        releases: ReleaseIntelligence | None,
        dependencies: DependencyIntelligence | None,
    ) -> str:
        """Classify repository quality and risk from existing model signals."""

        if dependencies and (
            dependencies.supply_chain_risk_score >= 75
            or dependencies.typosquatting_indicators
            or dependencies.suspicious_package_names
        ):
            return "Suspicious"
        if commits and commits.abandoned_repository:
            return "Abandoned"
        if dependencies and dependencies.supply_chain_risk_score >= 60:
            return "High Risk"
        if overall < 40 and confidence >= 50:
            return "High Risk"
        if commits and commits.dormant_development:
            return "Dormant"
        if confidence < 35:
            return "Experimental"
        if releases and releases.never_released_repository:
            return "Early Stage"
        if overall >= 85:
            return "High Quality"
        if overall >= 65:
            return "Promising"
        if overall >= 50:
            return "Early Stage"
        return "Experimental"

    @staticmethod
    def _repository_quality(repository: RepositoryAnalysis) -> ScoreExplanation:
        factors: list[str] = [
            f"{len(repository.technologies)} detected technologies"
        ]
        bonuses: list[str] = []
        penalties: list[str] = []
        score = 40.0 + min(15.0, len(repository.technologies) * 3.0)
        metadata = repository.metadata
        if metadata.get("description"):
            score += 15
            bonuses.append("repository description is present (+15)")
        else:
            score -= 10
            penalties.append("repository description is missing (-10)")
        if metadata.get("license"):
            score += 15
            bonuses.append("recognized license is present (+15)")
        else:
            score -= 10
            penalties.append("recognized license is missing (-10)")
        if metadata.get("default_branch"):
            score += 5
            bonuses.append("default branch is configured (+5)")
        if not repository.repository.private:
            score += 10
            bonuses.append("repository is publicly inspectable (+10)")
        else:
            score -= 10
            penalties.append("private visibility limits evidence (-10)")
        return ScoreExplanation(
            score=RepositoryScoringEngine._clamp(score),
            contributing_factors=tuple(factors),
            penalties=tuple(penalties),
            bonuses=tuple(bonuses),
            confidence=85.0,
            evidence_sources=("RepositoryAnalysis.metadata", "Repository model"),
        )

    @staticmethod
    def _organization_quality(
        organization: "OrganizationIntelligence | None",
    ) -> ScoreExplanation:
        if organization is None:
            return RepositoryScoringEngine._unavailable("OrganizationIntelligence")
        score = 30.0
        bonuses: list[str] = []
        penalties: list[str] = []
        factors = [
            f"{organization.repository_count} public repositories",
            f"{organization.followers} followers",
        ]
        if organization.verified:
            score += 20
            bonuses.append("GitHub organization is verified (+20)")
        else:
            penalties.append("organization is not verified")
        score += min(20.0, organization.repository_count / 2)
        score += min(15.0, organization.followers / 100)
        if organization.public_member_count:
            score += min(10.0, organization.public_member_count)
            bonuses.append("public organization membership is visible (up to +10)")
        if organization.description and organization.website:
            score += 5
            bonuses.append("organization identity is complete (+5)")
        return ScoreExplanation(
            score=RepositoryScoringEngine._clamp(score),
            contributing_factors=tuple(factors),
            penalties=tuple(penalties),
            bonuses=tuple(bonuses),
            confidence=90.0,
            evidence_sources=("OrganizationIntelligence",),
        )

    @staticmethod
    def _contributor_quality(
        contributors: list[ContributorIntelligence],
    ) -> ScoreExplanation:
        if not contributors:
            return RepositoryScoringEngine._unavailable("ContributorIntelligence")
        humans = [value for value in contributors if not value.is_bot]
        diversity = mean(value.contributor_diversity_score for value in contributors)
        activity = mean(value.maintainer_activity_score for value in humans) if humans else 0.0
        bus_factor = max(value.repository_bus_factor for value in contributors)
        score = (
            diversity * 0.35
            + activity * 0.30
            + min(100.0, bus_factor * 25.0) * 0.20
            + min(100.0, len(humans) * 12.5) * 0.15
        )
        penalties: list[str] = []
        bonuses: list[str] = []
        if any(value.single_maintainer_risk for value in contributors):
            score -= 20
            penalties.append("single-maintainer risk detected (-20)")
        if bus_factor >= 3:
            score += 5
            bonuses.append("bus factor is at least three (+5)")
        return ScoreExplanation(
            score=RepositoryScoringEngine._clamp(score),
            contributing_factors=(
                f"contributor diversity score {diversity:.2f}",
                f"maintainer activity score {activity:.2f}",
                f"repository bus factor {bus_factor}",
                f"{len(humans)} human contributors",
            ),
            penalties=tuple(penalties),
            bonuses=tuple(bonuses),
            confidence=95.0,
            evidence_sources=("ContributorIntelligence",),
        )

    @staticmethod
    def _development_activity(
        commits: CommitIntelligence | None,
    ) -> ScoreExplanation:
        if commits is None:
            return RepositoryScoringEngine._unavailable("CommitIntelligence")
        score = (
            commits.commit_health_score * 0.4
            + commits.development_velocity_score * 0.2
            + commits.repository_freshness_score * 0.2
            + commits.development_consistency_score * 0.2
        )
        penalties: list[str] = []
        bonuses: list[str] = []
        if commits.abandoned_repository:
            score -= 35
            penalties.append("repository is abandoned (-35)")
        elif commits.dormant_development:
            score -= 20
            penalties.append("development is dormant (-20)")
        if commits.fake_activity_spikes or commits.mass_generated_commits:
            score -= 15
            penalties.append("potentially artificial commit activity (-15)")
        if commits.sustained_development:
            score += 10
            bonuses.append("sustained development detected (+10)")
        return ScoreExplanation(
            score=RepositoryScoringEngine._clamp(score),
            contributing_factors=(
                f"commit health {commits.commit_health_score:.2f}",
                f"development velocity {commits.development_velocity_score:.2f}",
                f"repository freshness {commits.repository_freshness_score:.2f}",
                f"development consistency {commits.development_consistency_score:.2f}",
            ),
            penalties=tuple(penalties),
            bonuses=tuple(bonuses),
            confidence=100.0,
            evidence_sources=("CommitIntelligence",),
        )

    @staticmethod
    def _release_quality(
        releases: ReleaseIntelligence | None,
    ) -> ScoreExplanation:
        if releases is None:
            return RepositoryScoringEngine._unavailable("ReleaseIntelligence")
        score = (
            releases.release_health_score * 0.35
            + releases.release_consistency_score * 0.15
            + releases.maintenance_score * 0.15
            + releases.project_maturity_score * 0.15
            + releases.version_quality_score * 0.10
            + releases.stability_score * 0.10
        )
        penalties: list[str] = []
        bonuses: list[str] = []
        if releases.never_released_repository:
            score -= 20
            penalties.append("repository has never published a release (-20)")
        if releases.abandoned_releases or releases.stalled_maintenance:
            score -= 20
            penalties.append("release maintenance is stalled or abandoned (-20)")
        if releases.release_adoption_readiness:
            score += 10
            bonuses.append("release is adoption-ready (+10)")
        return ScoreExplanation(
            score=RepositoryScoringEngine._clamp(score),
            contributing_factors=(
                f"release health {releases.release_health_score:.2f}",
                f"release consistency {releases.release_consistency_score:.2f}",
                f"project maturity {releases.project_maturity_score:.2f}",
                f"version quality {releases.version_quality_score:.2f}",
            ),
            penalties=tuple(penalties),
            bonuses=tuple(bonuses),
            confidence=95.0,
            evidence_sources=("ReleaseIntelligence",),
        )

    @staticmethod
    def _dependency_health(
        dependencies: DependencyIntelligence | None,
    ) -> ScoreExplanation:
        if dependencies is None:
            return RepositoryScoringEngine._unavailable("DependencyIntelligence")
        penalties: list[str] = []
        if dependencies.outdated_dependencies:
            penalties.append(
                f"{len(dependencies.outdated_dependencies)} outdated dependencies"
            )
        if dependencies.abandoned_dependencies:
            penalties.append(
                f"{len(dependencies.abandoned_dependencies)} abandoned dependencies"
            )
        return ScoreExplanation(
            score=RepositoryScoringEngine._clamp(
                dependencies.dependency_health_score
            ),
            contributing_factors=(
                f"package freshness {dependencies.package_freshness_score:.2f}",
                f"ecosystem maturity {dependencies.ecosystem_maturity_score:.2f}",
                f"dependency complexity {dependencies.dependency_complexity_score:.2f}",
            ),
            penalties=tuple(penalties),
            bonuses=(),
            confidence=90.0,
            evidence_sources=("DependencyIntelligence",),
        )

    @staticmethod
    def _supply_chain_risk(
        dependencies: DependencyIntelligence | None,
    ) -> ScoreExplanation:
        if dependencies is None:
            return RepositoryScoringEngine._unavailable("DependencyIntelligence")
        penalties = tuple(
            value
            for condition, value in (
                (dependencies.deprecated_packages, "deprecated packages detected"),
                (dependencies.archived_packages, "archived packages detected"),
                (dependencies.typosquatting_indicators, "typosquatting indicators detected"),
                (dependencies.suspicious_package_names, "suspicious package names detected"),
                (dependencies.dependency_explosion, "dependency explosion detected"),
            )
            if condition
        )
        return ScoreExplanation(
            score=RepositoryScoringEngine._clamp(
                dependencies.supply_chain_risk_score
            ),
            contributing_factors=(
                f"raw supply-chain risk {dependencies.supply_chain_risk_score:.2f}",
            ),
            penalties=penalties,
            bonuses=("no identified supply-chain risks",) if not penalties else (),
            confidence=90.0,
            evidence_sources=("DependencyIntelligence",),
        )

    @staticmethod
    def _documentation(
        repository: RepositoryAnalysis,
        supplied_score: float | None,
    ) -> ScoreExplanation:
        if supplied_score is not None:
            return ScoreExplanation(
                score=RepositoryScoringEngine._clamp(supplied_score),
                contributing_factors=("external documentation score supplied",),
                penalties=(),
                bonuses=(),
                confidence=90.0,
                evidence_sources=("supplied documentation intelligence",),
            )
        metadata = repository.metadata
        checks = {
            "description": bool(metadata.get("description")),
            "homepage": bool(metadata.get("homepage")),
            "topics": bool(metadata.get("topics")),
            "license": bool(metadata.get("license")),
        }
        score = sum(checks.values()) / len(checks) * 100.0
        return ScoreExplanation(
            score=round(score, 2),
            contributing_factors=tuple(
                f"{name} metadata is present" for name, present in checks.items() if present
            ),
            penalties=tuple(
                f"{name} metadata is missing" for name, present in checks.items() if not present
            ),
            bonuses=(),
            confidence=60.0,
            evidence_sources=("RepositoryAnalysis.metadata",),
        )

    @staticmethod
    def _placeholder(name: str) -> ScoreExplanation:
        return ScoreExplanation(
            score=50.0,
            contributing_factors=(f"neutral placeholder for future {name}",),
            penalties=(),
            bonuses=(),
            confidence=0.0,
            evidence_sources=("placeholder",),
        )

    @staticmethod
    def _unavailable(source: str) -> ScoreExplanation:
        return ScoreExplanation(
            score=50.0,
            contributing_factors=(f"{source} was not supplied; neutral score used",),
            penalties=(),
            bonuses=(),
            confidence=0.0,
            evidence_sources=(f"missing {source}",),
        )

    @staticmethod
    def _clamp(value: float) -> float:
        return round(max(0.0, min(100.0, float(value))), 2)
