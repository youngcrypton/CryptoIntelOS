"""Independent reusable rules for repository intelligence signals."""

from ..activity.activity_profile import ActivityProfile
from ..contributors.contributor_profile import ContributorProfile
from ..organizations.organization_profile import OrganizationProfile
from ..analysis.repository_analyzer import RepositoryAnalysis
from .signal_models import SignalEvidence


class SignalRules:
    """Evaluate profile facts and return confidence with supporting evidence."""

    @staticmethod
    def high_developer_activity(activity: ActivityProfile) -> tuple[float, list[SignalEvidence]]:
        """Detect sustained commit activity and multiple contributors."""

        commits = int(activity.commit_metrics.get("commit_count", 0))
        contributors = len(activity.commit_metrics.get("contributor_activity", {}))
        confidence = min(1.0, (commits / 20) * 0.7 + (contributors / 4) * 0.3)
        evidence = [
            SignalEvidence("commits", f"{commits} commits recorded"),
            SignalEvidence("contributors", f"{contributors} active contributors"),
        ]
        return confidence, evidence

    @staticmethod
    def rapid_release_cycle(activity: ActivityProfile) -> tuple[float, list[SignalEvidence]]:
        """Detect a project with a recurring release cadence."""

        releases = int(activity.release_metrics.get("release_count", 0))
        confidence = min(1.0, releases / 6)
        return confidence, [SignalEvidence("releases", f"{releases} releases recorded")]

    @staticmethod
    def experienced_team(contributor: ContributorProfile) -> tuple[float, list[SignalEvidence]]:
        """Detect contributors with established accounts and public work."""

        age = contributor.activity_summary.get("account_age_days") or 0
        repositories = contributor.contributor_metadata.get("public_repository_count", 0)
        confidence = min(1.0, (float(age) / 1460) * 0.6 + (int(repositories) / 20) * 0.4)
        return confidence, [
            SignalEvidence("account_age", f"{age} account age days"),
            SignalEvidence("public_repositories", f"{repositories} public repositories"),
        ]

    @staticmethod
    def active_organization(organization: OrganizationProfile) -> tuple[float, list[SignalEvidence]]:
        """Detect organizations with active, non-archived repositories."""

        repositories = organization.repository_statistics.get("repository_count", 0)
        active = organization.activity_summary.get("active_repositories", 0)
        confidence = min(1.0, (int(repositories) / 10) * 0.5 + (int(active) / 10) * 0.5)
        return confidence, [
            SignalEvidence("repositories", f"{repositories} organization repositories"),
            SignalEvidence("activity", f"{active} active repositories"),
        ]

    @staticmethod
    def early_stage_project(repository: RepositoryAnalysis) -> tuple[float, list[SignalEvidence]]:
        """Detect low-scale repositories that may be early in development."""

        stars = int(repository.activity_metrics.get("stars", 0))
        commits = int(repository.activity_metrics.get("commit_count", 0))
        confidence = max(0.0, 1.0 - min(1.0, stars / 500) * 0.5 - min(1.0, commits / 100) * 0.5)
        return confidence, [
            SignalEvidence("stars", f"{stars} repository stars"),
            SignalEvidence("commits", f"{commits} commits recorded"),
        ]

    @staticmethod
    def dormant_project(activity: ActivityProfile) -> tuple[float, list[SignalEvidence]]:
        """Detect stale development indicators."""

        indicators = activity.commit_metrics.get("development_trend_indicators", [])
        dormant = "stale_activity" in indicators or "no_timestamped_commits" in indicators
        return (1.0 if dormant else 0.0), [
            SignalEvidence("development_trend", ", ".join(indicators) or "no trend data")
        ]

    @staticmethod
    def security_focused(repository: RepositoryAnalysis) -> tuple[float, list[SignalEvidence]]:
        """Detect security-oriented technologies, topics, or metadata."""

        values = [value.lower() for value in repository.technologies]
        matches = [value for value in values if "security" in value or "audit" in value]
        confidence = min(1.0, len(matches) / 2)
        return confidence, [SignalEvidence("technology", value) for value in matches]

    @staticmethod
    def open_source_healthy(repository: RepositoryAnalysis) -> tuple[float, list[SignalEvidence]]:
        """Detect a public repository with meaningful activity and community use."""

        stars = int(repository.activity_metrics.get("stars", 0))
        forks = int(repository.activity_metrics.get("forks", 0))
        public = repository.metadata.get("visibility") == "public"
        confidence = min(1.0, (0.4 if public else 0) + min(stars / 500, 0.3) + min(forks / 100, 0.3))
        return confidence, [
            SignalEvidence("visibility", str(repository.metadata.get("visibility"))),
            SignalEvidence("community", f"{stars} stars and {forks} forks"),
        ]
