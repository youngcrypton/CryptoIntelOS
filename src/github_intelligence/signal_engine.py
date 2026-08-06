"""Explainable rule-based signals from existing GitHub intelligence models."""

from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from .analysis.repository_analyzer import RepositoryAnalysis
from .commit_analyzer import CommitIntelligence
from .contributor_analyzer import ContributorIntelligence
from .dependency_analyzer import DependencyIntelligence
from .release_analyzer import ReleaseIntelligence
from .repository_scoring import RepositoryScore, ScoreExplanation

if TYPE_CHECKING:
    from .organization_analyzer import OrganizationIntelligence


SignalMetric = int | float | str | bool | None


@dataclass(frozen=True)
class GitHubIntelligenceSignal:
    """One structured and fully explainable GitHub intelligence signal."""

    signal_id: str
    signal_name: str
    category: str
    severity: str
    confidence: float
    supporting_evidence: tuple[str, ...]
    contributing_metrics: dict[str, SignalMetric]
    explanation: str
    timestamp: datetime
    source_analyzers: tuple[str, ...]
    repository_score_components: dict[str, float]


@dataclass(frozen=True)
class SignalContext:
    """Existing Phase 2 intelligence available to registered signal rules."""

    repository: RepositoryAnalysis
    organization: "OrganizationIntelligence | None"
    contributors: tuple[ContributorIntelligence, ...]
    commits: CommitIntelligence | None
    releases: ReleaseIntelligence | None
    dependencies: DependencyIntelligence | None
    repository_score: RepositoryScore


@dataclass(frozen=True)
class SignalRuleMatch:
    """Evidence returned by a rule when its transparent condition matches."""

    supporting_evidence: tuple[str, ...]
    contributing_metrics: dict[str, SignalMetric]
    explanation: str
    score_components: tuple[str, ...]
    evidence_strength: float


SignalEvaluator = Callable[[SignalContext], SignalRuleMatch | None]


@dataclass(frozen=True)
class GitHubSignalRule:
    """Declarative registry entry for one independently extensible signal rule."""

    signal_id: str
    signal_name: str
    category: str
    source_analyzers: tuple[str, ...]
    evaluator: SignalEvaluator
    risk_signal: bool = False


class GitHubSignalEngine:
    """Evaluate registered rules against existing intelligence without collection."""

    _SCORE_COMPONENTS: dict[str, str] = {
        "repository_quality": "repository_quality_score",
        "organization_quality": "organization_quality_score",
        "contributor_quality": "contributor_quality_score",
        "development_activity": "development_activity_score",
        "release_quality": "release_quality_score",
        "dependency_health": "dependency_health_score",
        "supply_chain_risk": "supply_chain_risk_score",
        "documentation": "documentation_score",
        "security": "security_score",
        "governance": "governance_score",
    }

    def __init__(self, rules: Iterable[GitHubSignalRule] | None = None) -> None:
        """Initialize with default rules or a supplied independent rule set."""

        selected_rules = self.default_rules() if rules is None else tuple(rules)
        self._rules: dict[str, GitHubSignalRule] = {}
        for rule in selected_rules:
            self.register_rule(rule)

    def register_rule(
        self, rule: GitHubSignalRule, *, replace: bool = False
    ) -> None:
        """Register an additional rule without modifying engine evaluation logic."""

        if rule.signal_id in self._rules and not replace:
            raise ValueError(f"signal rule already registered: {rule.signal_id}")
        self._rules[rule.signal_id] = rule

    def generate(
        self,
        repository: RepositoryAnalysis,
        repository_score: RepositoryScore,
        organization: "OrganizationIntelligence | None" = None,
        contributors: Iterable[ContributorIntelligence] | None = None,
        commits: CommitIntelligence | None = None,
        releases: ReleaseIntelligence | None = None,
        dependencies: DependencyIntelligence | None = None,
        timestamp: datetime | None = None,
    ) -> list[GitHubIntelligenceSignal]:
        """Generate all matching signals from supplied Phase 2 intelligence."""

        context = SignalContext(
            repository=repository,
            organization=organization,
            contributors=tuple(
                contributors
                if contributors is not None
                else repository.contributor_intelligence
            ),
            commits=commits or repository.commit_intelligence,
            releases=releases or repository.release_intelligence,
            dependencies=dependencies or repository.dependency_intelligence,
            repository_score=repository_score,
        )
        generated_at = self._as_utc(timestamp or datetime.now(timezone.utc))
        signals: list[GitHubIntelligenceSignal] = []
        for rule in self._rules.values():
            match = rule.evaluator(context)
            if match is None:
                continue
            score_components = self.aggregate_score_evidence(
                repository_score, match.score_components
            )
            confidence = self.calculate_confidence(
                repository_score, match.score_components, match.evidence_strength
            )
            signals.append(
                GitHubIntelligenceSignal(
                    signal_id=rule.signal_id,
                    signal_name=rule.signal_name,
                    category=rule.category,
                    severity=self.classify_severity(
                        match.evidence_strength, rule.risk_signal
                    ),
                    confidence=confidence,
                    supporting_evidence=match.supporting_evidence,
                    contributing_metrics=dict(match.contributing_metrics),
                    explanation=match.explanation,
                    timestamp=generated_at,
                    source_analyzers=rule.source_analyzers,
                    repository_score_components=score_components,
                )
            )
        return signals

    @classmethod
    def calculate_confidence(
        cls,
        repository_score: RepositoryScore,
        components: Iterable[str],
        evidence_strength: float,
    ) -> float:
        """Correlate evidence strength with relevant scoring confidence."""

        explanations = cls._component_explanations(repository_score, components)
        component_confidence = (
            sum(value.confidence for value in explanations) / len(explanations)
            if explanations
            else repository_score.confidence_score
        )
        confidence = component_confidence * 0.7 + cls._clamp(evidence_strength) * 0.3
        return round(cls._clamp(confidence), 2)

    @classmethod
    def aggregate_score_evidence(
        cls,
        repository_score: RepositoryScore,
        components: Iterable[str],
    ) -> dict[str, float]:
        """Return the exact repository score components referenced by a signal."""

        evidence: dict[str, float] = {}
        for component in components:
            attribute = cls._SCORE_COMPONENTS.get(component)
            if attribute is None:
                raise ValueError(f"unknown repository score component: {component}")
            explanation = getattr(repository_score, attribute)
            evidence[component] = explanation.score
        evidence["overall_repository_score"] = repository_score.overall_repository_score
        return evidence

    @staticmethod
    def classify_severity(evidence_strength: float, risk_signal: bool = False) -> str:
        """Classify severity consistently for positive and risk-oriented signals."""

        strength = GitHubSignalEngine._clamp(evidence_strength)
        if risk_signal:
            if strength >= 90:
                return "critical"
            if strength >= 70:
                return "high"
            if strength >= 45:
                return "medium"
            return "low"
        if strength >= 85:
            return "high"
        if strength >= 60:
            return "medium"
        return "informational"

    @classmethod
    def default_rules(cls) -> tuple[GitHubSignalRule, ...]:
        """Return independent built-in rules; callers may extend or replace them."""

        return (
            cls._rule("EARLY_BUILDER", "Early Builder", "lifecycle", ("CommitAnalyzer", "ReleaseAnalyzer", "RepositoryScoringEngine"), cls._early_builder),
            cls._rule("ACTIVE_DEVELOPMENT", "Active Development", "development", ("CommitAnalyzer", "RepositoryScoringEngine"), cls._active_development),
            cls._rule("HIGH_DEVELOPMENT_VELOCITY", "High Development Velocity", "development", ("CommitAnalyzer", "RepositoryScoringEngine"), cls._high_velocity),
            cls._rule("DORMANT_PROJECT", "Dormant Project", "risk", ("CommitAnalyzer", "RepositoryScoringEngine"), cls._dormant, True),
            cls._rule("ABANDONED_REPOSITORY", "Abandoned Repository", "risk", ("CommitAnalyzer", "RepositoryScoringEngine"), cls._abandoned, True),
            cls._rule("STRONG_ORGANIZATION", "Strong Organization", "organization", ("OrganizationAnalyzer", "RepositoryScoringEngine"), cls._strong_organization),
            cls._rule("STRONG_CONTRIBUTOR_BASE", "Strong Contributor Base", "contributors", ("ContributorAnalyzer", "RepositoryScoringEngine"), cls._strong_contributors),
            cls._rule("HEALTHY_RELEASE_CADENCE", "Healthy Release Cadence", "release", ("ReleaseAnalyzer", "RepositoryScoringEngine"), cls._healthy_releases),
            cls._rule("SUPPLY_CHAIN_RISK", "Supply Chain Risk", "risk", ("DependencyAnalyzer", "RepositoryScoringEngine"), cls._supply_chain_risk, True),
            cls._rule("DEPENDENCY_RISK", "Dependency Risk", "risk", ("DependencyAnalyzer", "RepositoryScoringEngine"), cls._dependency_risk, True),
            cls._rule("SINGLE_MAINTAINER_RISK", "Single Maintainer Risk", "risk", ("ContributorAnalyzer", "CommitAnalyzer", "RepositoryScoringEngine"), cls._single_maintainer, True),
            cls._rule("CORE_TEAM_GROWTH", "Core Team Growth", "contributors", ("ContributorAnalyzer", "CommitAnalyzer", "RepositoryScoringEngine"), cls._core_team_growth),
            cls._rule("EMERGING_PROJECT", "Emerging Project", "lifecycle", ("CommitAnalyzer", "ReleaseAnalyzer", "RepositoryScoringEngine"), cls._emerging),
            cls._rule("MATURE_PROJECT", "Mature Project", "lifecycle", ("ReleaseAnalyzer", "RepositoryScoringEngine"), cls._mature),
            cls._rule("EXPERIMENTAL_PROJECT", "Experimental Project", "lifecycle", ("ReleaseAnalyzer", "RepositoryScoringEngine"), cls._experimental),
            cls._rule("INFRASTRUCTURE_PROJECT", "Infrastructure Project", "classification", ("RepositoryAnalyzer", "RepositoryScoringEngine"), cls._infrastructure),
            cls._rule("HIGH_CONFIDENCE_PROJECT", "High Confidence Project", "quality", ("RepositoryScoringEngine",), cls._high_confidence),
            cls._rule("WATCHLIST_CANDIDATE", "Watchlist Candidate", "monitoring", ("RepositoryScoringEngine", "CommitAnalyzer", "DependencyAnalyzer"), cls._watchlist),
        )

    @staticmethod
    def _rule(
        signal_id: str,
        name: str,
        category: str,
        sources: tuple[str, ...],
        evaluator: SignalEvaluator,
        risk: bool = False,
    ) -> GitHubSignalRule:
        return GitHubSignalRule(signal_id, name, category, sources, evaluator, risk)

    @staticmethod
    def _early_builder(context: SignalContext) -> SignalRuleMatch | None:
        commits, releases = context.commits, context.releases
        if not commits or commits.repository_age > 365 or not commits.active_development:
            return None
        release_count = releases.total_releases if releases else 0
        if release_count > 2:
            return None
        strength = min(90.0, 60.0 + commits.development_velocity_score * 0.3)
        return GitHubSignalEngine._match(
            (f"repository age is {commits.repository_age} days", f"{release_count} releases published", "development is active"),
            {"repository_age_days": commits.repository_age, "total_releases": release_count, "velocity_score": commits.development_velocity_score},
            "A young repository is actively building before establishing a mature release history.",
            ("development_activity", "release_quality"), strength,
        )

    @staticmethod
    def _active_development(context: SignalContext) -> SignalRuleMatch | None:
        value = context.commits
        if not value or not value.active_development:
            return None
        return GitHubSignalEngine._match(
            (f"{value.commits_last_30_days} commits in 30 days", f"latest commit was {value.days_since_last_commit} days ago"),
            {"commits_last_30_days": value.commits_last_30_days, "days_since_last_commit": value.days_since_last_commit, "commit_health_score": value.commit_health_score},
            "Recent commit history demonstrates continuing repository development.",
            ("development_activity",), max(60.0, value.commit_health_score),
        )

    @staticmethod
    def _high_velocity(context: SignalContext) -> SignalRuleMatch | None:
        value = context.commits
        if not value or value.development_velocity_score < 75:
            return None
        return GitHubSignalEngine._match(
            (f"development velocity score is {value.development_velocity_score:.2f}", f"{value.commits_last_30_days} commits in 30 days"),
            {"development_velocity_score": value.development_velocity_score, "recent_activity_trend": value.recent_activity_trend},
            "Commit frequency and recent activity exceed the high-velocity threshold.",
            ("development_activity",), value.development_velocity_score,
        )

    @staticmethod
    def _dormant(context: SignalContext) -> SignalRuleMatch | None:
        value = context.commits
        if not value or not value.dormant_development:
            return None
        return GitHubSignalEngine._match(
            (f"latest commit was {value.days_since_last_commit} days ago", f"dormancy risk score is {value.dormancy_risk_score:.2f}"),
            {"days_since_last_commit": value.days_since_last_commit, "dormancy_risk_score": value.dormancy_risk_score},
            "Commit recency falls within the dormant-development range.",
            ("development_activity",), max(60.0, value.dormancy_risk_score),
        )

    @staticmethod
    def _abandoned(context: SignalContext) -> SignalRuleMatch | None:
        value = context.commits
        if not value or not value.abandoned_repository:
            return None
        return GitHubSignalEngine._match(
            (f"latest commit was {value.days_since_last_commit} days ago", "commit analyzer classified the repository as abandoned"),
            {"days_since_last_commit": value.days_since_last_commit, "abandoned_maintenance": value.abandoned_maintenance},
            "The repository has exceeded the abandonment threshold without development activity.",
            ("development_activity",), 95.0,
        )

    @staticmethod
    def _strong_organization(context: SignalContext) -> SignalRuleMatch | None:
        score = context.repository_score.organization_quality_score
        if context.organization is None or score.score < 75:
            return None
        return GitHubSignalEngine._match(
            (f"organization quality score is {score.score:.2f}", f"organization has {context.organization.followers} followers", f"organization verification is {context.organization.verified}"),
            {"organization_quality_score": score.score, "followers": context.organization.followers, "verified": context.organization.verified},
            "Organization identity, legitimacy, and public presence exceed the strong-organization threshold.",
            ("organization_quality",), score.score,
        )

    @staticmethod
    def _strong_contributors(context: SignalContext) -> SignalRuleMatch | None:
        score = context.repository_score.contributor_quality_score
        if not context.contributors or score.score < 70:
            return None
        humans = sum(not value.is_bot for value in context.contributors)
        bus_factor = max(value.repository_bus_factor for value in context.contributors)
        return GitHubSignalEngine._match(
            (f"contributor quality score is {score.score:.2f}", f"{humans} human contributors", f"repository bus factor is {bus_factor}"),
            {"contributor_quality_score": score.score, "human_contributors": humans, "bus_factor": bus_factor},
            "Contributor diversity, activity, and resilience form a strong contributor base.",
            ("contributor_quality",), score.score,
        )

    @staticmethod
    def _healthy_releases(context: SignalContext) -> SignalRuleMatch | None:
        value = context.releases
        if not value or value.release_health_score < 70 or value.irregular_release_schedule:
            return None
        return GitHubSignalEngine._match(
            (f"release health score is {value.release_health_score:.2f}", f"release cadence is {value.release_cadence}", f"release consistency score is {value.release_consistency_score:.2f}"),
            {"release_health_score": value.release_health_score, "release_consistency_score": value.release_consistency_score, "release_frequency": value.release_frequency},
            "Release health and consistency indicate a dependable software delivery cadence.",
            ("release_quality",), value.release_health_score,
        )

    @staticmethod
    def _supply_chain_risk(context: SignalContext) -> SignalRuleMatch | None:
        value = context.dependencies
        if not value or value.supply_chain_risk_score < 45:
            return None
        return GitHubSignalEngine._match(
            (f"supply-chain risk score is {value.supply_chain_risk_score:.2f}", f"{len(value.typosquatting_indicators)} typosquatting indicators", f"{len(value.suspicious_package_names)} suspicious package names"),
            {"supply_chain_risk_score": value.supply_chain_risk_score, "typosquatting_count": len(value.typosquatting_indicators), "suspicious_package_count": len(value.suspicious_package_names)},
            "Dependency intelligence identifies material software supply-chain exposure.",
            ("supply_chain_risk", "dependency_health"), value.supply_chain_risk_score,
        )

    @staticmethod
    def _dependency_risk(context: SignalContext) -> SignalRuleMatch | None:
        value = context.dependencies
        if not value or (value.dependency_health_score >= 50 and not value.outdated_dependencies and not value.abandoned_dependencies):
            return None
        strength = max(50.0, 100.0 - value.dependency_health_score)
        return GitHubSignalEngine._match(
            (f"dependency health score is {value.dependency_health_score:.2f}", f"{len(value.outdated_dependencies)} outdated dependencies", f"{len(value.abandoned_dependencies)} abandoned dependencies"),
            {"dependency_health_score": value.dependency_health_score, "outdated_count": len(value.outdated_dependencies), "abandoned_count": len(value.abandoned_dependencies)},
            "Dependency freshness or maintenance quality falls below healthy thresholds.",
            ("dependency_health", "supply_chain_risk"), strength,
        )

    @staticmethod
    def _single_maintainer(context: SignalContext) -> SignalRuleMatch | None:
        contributor_risk = any(value.single_maintainer_risk for value in context.contributors)
        commit_risk = bool(context.commits and context.commits.single_developer_dependency)
        if not contributor_risk and not commit_risk:
            return None
        concentration = context.commits.maintainer_activity_concentration if context.commits else None
        return GitHubSignalEngine._match(
            ("contributor intelligence detected single-maintainer risk" if contributor_risk else "commit distribution is concentrated in one developer", f"maintainer commit concentration is {concentration}"),
            {"contributor_single_maintainer_risk": contributor_risk, "commit_single_developer_dependency": commit_risk, "maintainer_activity_concentration": concentration},
            "Repository continuity depends excessively on one maintainer or developer.",
            ("contributor_quality", "development_activity"), max(75.0, float(concentration or 0)),
        )

    @staticmethod
    def _core_team_growth(context: SignalContext) -> SignalRuleMatch | None:
        core = [value for value in context.contributors if value.is_core_maintainer and not value.is_bot]
        if len(core) < 3 or not context.commits or not context.commits.accelerating_activity:
            return None
        strength = min(95.0, 60.0 + len(core) * 8.0)
        return GitHubSignalEngine._match(
            (f"{len(core)} active core maintainers", f"recent activity trend is {context.commits.recent_activity_trend:.2f}%"),
            {"core_maintainers": len(core), "recent_activity_trend": context.commits.recent_activity_trend},
            "A multi-person core team is paired with accelerating commit activity.",
            ("contributor_quality", "development_activity"), strength,
        )

    @staticmethod
    def _emerging(context: SignalContext) -> SignalRuleMatch | None:
        classification = context.repository_score.risk_classification
        if classification not in {"Promising", "Early Stage"} or not context.commits or not context.commits.active_development:
            return None
        return GitHubSignalEngine._match(
            (f"repository classification is {classification}", "development is active", f"overall score is {context.repository_score.overall_repository_score:.2f}"),
            {"overall_repository_score": context.repository_score.overall_repository_score, "classification": classification, "commits_last_30_days": context.commits.commits_last_30_days},
            "An active early or promising repository is showing evidence of emergence.",
            ("repository_quality", "development_activity", "release_quality"), max(60.0, context.repository_score.overall_repository_score),
        )

    @staticmethod
    def _mature(context: SignalContext) -> SignalRuleMatch | None:
        value = context.releases
        if not value or (value.project_maturity_score < 75 and context.repository_score.overall_repository_score < 85):
            return None
        strength = max(value.project_maturity_score, context.repository_score.overall_repository_score)
        return GitHubSignalEngine._match(
            (f"project maturity score is {value.project_maturity_score:.2f}", f"{value.stable_release_count} stable releases", f"overall score is {context.repository_score.overall_repository_score:.2f}"),
            {"project_maturity_score": value.project_maturity_score, "stable_release_count": value.stable_release_count, "overall_repository_score": context.repository_score.overall_repository_score},
            "Release history and repository quality indicate an established mature project.",
            ("release_quality", "repository_quality"), strength,
        )

    @staticmethod
    def _experimental(context: SignalContext) -> SignalRuleMatch | None:
        prerelease_heavy = bool(context.releases and context.releases.excessive_prereleases)
        if context.repository_score.risk_classification != "Experimental" and not prerelease_heavy:
            return None
        return GitHubSignalEngine._match(
            (f"repository classification is {context.repository_score.risk_classification}", f"confidence score is {context.repository_score.confidence_score:.2f}", f"excessive prereleases is {prerelease_heavy}"),
            {"overall_repository_score": context.repository_score.overall_repository_score, "confidence_score": context.repository_score.confidence_score, "excessive_prereleases": prerelease_heavy},
            "Available evidence indicates an experimental project with limited maturity or confidence.",
            ("repository_quality", "release_quality"), max(45.0, 100.0 - context.repository_score.confidence_score),
        )

    @staticmethod
    def _infrastructure(context: SignalContext) -> SignalRuleMatch | None:
        metadata = context.repository.metadata
        values = [
            *context.repository.technologies,
            str(metadata.get("description") or ""),
            *(str(value) for value in metadata.get("topics", []) if value),
        ]
        keywords = ("infrastructure", "protocol", "node", "rpc", "sdk", "blockchain", "indexer", "consensus")
        matches = sorted({keyword for value in values for keyword in keywords if keyword in value.casefold()})
        if not matches:
            return None
        strength = min(90.0, 50.0 + len(matches) * 10.0)
        return GitHubSignalEngine._match(
            tuple(f"repository metadata contains infrastructure term '{value}'" for value in matches),
            {"matched_infrastructure_terms": len(matches), "technology_count": len(context.repository.technologies)},
            "Repository technologies and metadata identify infrastructure-oriented software.",
            ("repository_quality", "documentation"), strength,
        )

    @staticmethod
    def _high_confidence(context: SignalContext) -> SignalRuleMatch | None:
        value = context.repository_score.confidence_score
        if value < 80:
            return None
        return GitHubSignalEngine._match(
            (f"repository confidence score is {value:.2f}", f"repository tier is {context.repository_score.repository_tier}"),
            {"confidence_score": value, "overall_repository_score": context.repository_score.overall_repository_score},
            "Multiple Phase 2 analyzers provide sufficiently complete corroborating evidence.",
            tuple(GitHubSignalEngine._SCORE_COMPONENTS), value,
        )

    @staticmethod
    def _watchlist(context: SignalContext) -> SignalRuleMatch | None:
        overall = context.repository_score.overall_repository_score
        classification = context.repository_score.risk_classification
        active = bool(context.commits and context.commits.active_development)
        dependency_risk = context.dependencies.supply_chain_risk_score if context.dependencies else 0.0
        if not (50 <= overall < 85 and (active or classification in {"Promising", "Early Stage"}) or 40 <= dependency_risk < 75):
            return None
        strength = max(55.0, min(85.0, overall), dependency_risk)
        return GitHubSignalEngine._match(
            (f"overall score is {overall:.2f}", f"classification is {classification}", f"active development is {active}", f"supply-chain risk is {dependency_risk:.2f}"),
            {"overall_repository_score": overall, "classification": classification, "active_development": active, "supply_chain_risk_score": dependency_risk},
            "The repository has meaningful potential or moderate risk that warrants continued monitoring.",
            ("repository_quality", "development_activity", "supply_chain_risk"), strength,
        )

    @staticmethod
    def _match(
        evidence: tuple[str, ...],
        metrics: Mapping[str, SignalMetric],
        explanation: str,
        components: tuple[str, ...],
        strength: float,
    ) -> SignalRuleMatch:
        return SignalRuleMatch(
            supporting_evidence=evidence,
            contributing_metrics=dict(metrics),
            explanation=explanation,
            score_components=components,
            evidence_strength=GitHubSignalEngine._clamp(strength),
        )

    @classmethod
    def _component_explanations(
        cls, repository_score: RepositoryScore, components: Iterable[str]
    ) -> list[ScoreExplanation]:
        explanations: list[ScoreExplanation] = []
        for component in components:
            attribute = cls._SCORE_COMPONENTS.get(component)
            if attribute is None:
                raise ValueError(f"unknown repository score component: {component}")
            explanations.append(getattr(repository_score, attribute))
        return explanations

    @staticmethod
    def _as_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    @staticmethod
    def _clamp(value: float) -> float:
        return max(0.0, min(100.0, float(value)))
