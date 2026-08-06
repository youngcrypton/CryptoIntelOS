"""Coordinator for GitHub intelligence signal generation."""

from datetime import datetime, timezone

from ..activity.activity_profile import ActivityProfile
from ..analysis.repository_analyzer import RepositoryAnalysis
from ..contributors.contributor_profile import ContributorProfile
from ..organizations.organization_profile import OrganizationProfile
from .signal_models import IntelligenceSignal, SignalReport
from .signal_rules import SignalRules


class SignalEngine:
    """Generate independent rule-based signals from existing analysis profiles."""

    def generate(
        self,
        repository: RepositoryAnalysis,
        organization: OrganizationProfile,
        contributor: ContributorProfile,
        activity: ActivityProfile,
    ) -> SignalReport:
        """Evaluate all Sprint 2.7 rules and return a timestamped report."""

        evaluations = [
            ("HIGH_DEVELOPER_ACTIVITY", SignalRules.high_developer_activity(activity)),
            ("RAPID_RELEASE_CYCLE", SignalRules.rapid_release_cycle(activity)),
            ("EXPERIENCED_TEAM", SignalRules.experienced_team(contributor)),
            ("ACTIVE_ORGANIZATION", SignalRules.active_organization(organization)),
            ("EARLY_STAGE_PROJECT", SignalRules.early_stage_project(repository)),
            ("DORMANT_PROJECT", SignalRules.dormant_project(activity)),
            ("SECURITY_FOCUSED", SignalRules.security_focused(repository)),
            ("OPEN_SOURCE_HEALTHY", SignalRules.open_source_healthy(repository)),
        ]
        signals = [
            IntelligenceSignal(name, round(confidence, 4), evidence)
            for name, (confidence, evidence) in evaluations
            if confidence > 0
        ]
        return SignalReport(
            generated_signals=signals,
            confidence_summary={signal.name: signal.confidence for signal in signals},
            evidence_summary=[evidence for signal in signals for evidence in signal.evidence],
            generation_timestamp=datetime.now(timezone.utc),
        )
