"""Contributor profile analysis."""

from collections.abc import Iterable, Mapping
from datetime import datetime, timezone
from typing import Any

from ..models import Contributor
from .contributor_profile import ContributorProfile


class ContributorAnalyzer:
    """Analyze contributor metadata and repository involvement."""

    def analyze(
        self,
        contributor: Contributor,
        metadata: Mapping[str, Any] | None = None,
        repositories: Iterable[Mapping[str, Any]] | None = None,
    ) -> ContributorProfile:
        """Create a contributor profile without commit intelligence or AI scoring."""

        raw_metadata = metadata or {}
        repository_list = list(repositories or [])
        organizations = self._organizations(raw_metadata)
        technologies = self._technologies(repository_list)
        contribution_count = self._integer(
            raw_metadata.get("contributions", contributor.contributions)
        )
        public_repository_count = self._integer(raw_metadata.get("public_repos", 0))
        return ContributorProfile(
            contributor=contributor,
            contributor_metadata={
                "name": raw_metadata.get("name"),
                "company": raw_metadata.get("company"),
                "location": raw_metadata.get("location"),
                "bio": raw_metadata.get("bio"),
                "followers": self._integer(raw_metadata.get("followers", 0)),
                "following": self._integer(raw_metadata.get("following", 0)),
                "public_repository_count": public_repository_count,
            },
            contribution_summary={
                "contributions": contribution_count,
                "repository_count": len(repository_list),
                "contribution_frequency": raw_metadata.get("contribution_frequency"),
            },
            repository_involvement=[
                str(repository.get("full_name", repository.get("name", "")))
                for repository in repository_list
                if repository.get("full_name") or repository.get("name")
            ],
            organization_affiliations=organizations,
            activity_summary={
                "account_age_days": self._account_age_days(raw_metadata.get("created_at")),
                "last_active": raw_metadata.get("updated_at"),
                "followers": self._integer(raw_metadata.get("followers", 0)),
            },
            technology_footprint=technologies,
        )

    @staticmethod
    def _organizations(metadata: Mapping[str, Any]) -> list[str]:
        """Extract organization logins or names from user metadata."""

        values = metadata.get("organizations", [])
        return [
            str(value.get("login", value.get("name", "")))
            if isinstance(value, Mapping)
            else str(value)
            for value in values
            if value
        ]

    @staticmethod
    def _technologies(repositories: list[Mapping[str, Any]]) -> list[str]:
        """Return unique languages and topics across involved repositories."""

        technologies: list[str] = []
        for repository in repositories:
            values = [repository.get("language"), *repository.get("topics", [])]
            for value in values:
                if isinstance(value, str) and value and value not in technologies:
                    technologies.append(value)
        return technologies

    @staticmethod
    def _integer(value: object) -> int:
        """Convert an API count safely."""

        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _account_age_days(created_at: object) -> int | None:
        """Calculate account age from a GitHub ISO timestamp."""

        if not isinstance(created_at, str):
            return None
        try:
            created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except ValueError:
            return None
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        return max(0, (datetime.now(timezone.utc) - created).days)
