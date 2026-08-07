from dataclasses import asdict
from datetime import UTC, datetime

from src.core_intelligence.models import Evidence
from src.github_intelligence.contributor_analyzer import ContributorIntelligence
from src.github_intelligence.organization_analyzer import OrganizationIntelligence


class GitHubEvidenceAdapter:
    """Translate source-specific contributor and organization intelligence."""

    def contributor(self, value: ContributorIntelligence, *, entity_reference: str) -> Evidence:
        payload = asdict(value)
        return Evidence(
            evidence_id=f"github:contributor:{value.github_id}",
            entity_reference=entity_reference,
            observation_reference=f"github:contributor:{value.github_id}",
            metric="contributor_profile",
            value=payload,
            confidence=value.contributor_diversity_score / 100,
            source="github",
            provenance={"adapter": "GitHubEvidenceAdapter", "login": value.username},
            timestamp=datetime.now(UTC),
        )

    def organization(self, value: OrganizationIntelligence, *, entity_reference: str) -> Evidence:
        return Evidence(
            evidence_id=f"github:organization:{value.id}",
            entity_reference=entity_reference,
            observation_reference=f"github:organization:{value.id}",
            metric="organization_profile",
            value=asdict(value),
            confidence=1.0,
            source="github",
            provenance={"adapter": "GitHubEvidenceAdapter", "login": value.login},
            timestamp=datetime.now(UTC),
        )
