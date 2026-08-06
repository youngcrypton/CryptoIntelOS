"""Organization profile analysis."""

from collections.abc import Iterable, Mapping
from typing import Any

from ..models import Organization, Repository
from .organization_profile import OrganizationProfile


class OrganizationAnalyzer:
    """Analyze organization metadata, repositories, technology, and activity."""

    def analyze(
        self,
        organization: Organization,
        repositories: Iterable[Repository],
        metadata: Mapping[str, Any] | None = None,
        repository_metadata: Iterable[Mapping[str, Any]] | None = None,
    ) -> OrganizationProfile:
        """Create a profile without contributor or intelligence scoring."""

        repository_list = list(repositories)
        raw_metadata = metadata or {}
        raw_repositories = list(repository_metadata or [])
        technologies = self._technology_profile(raw_repositories)
        repository_statistics = {
            "repository_count": len(repository_list),
            "total_stars": sum(self._integer(item.get("stargazers_count", 0)) for item in raw_repositories),
            "total_forks": sum(self._integer(item.get("forks_count", 0)) for item in raw_repositories),
        }
        activity_summary = {
            "active_repositories": sum(
                not bool(item.get("archived", False)) for item in raw_repositories
            ),
            "archived_repositories": sum(
                bool(item.get("archived", False)) for item in raw_repositories
            ),
            "last_updated": self._latest_update(raw_repositories),
        }
        organization_metadata = {
            "followers": self._integer(raw_metadata.get("followers", 0)),
            "following": self._integer(raw_metadata.get("following", 0)),
            "verified": bool(
                raw_metadata.get("is_verified", raw_metadata.get("verified", False))
            ),
            "description": raw_metadata.get("description", organization.description),
        }
        ecosystem_indicators = [
            f"{len(repository_list)} repositories",
            f"{len(technologies)} technologies",
        ]
        if organization_metadata["verified"]:
            ecosystem_indicators.append("verified organization")
        return OrganizationProfile(
            organization=organization,
            organization_metadata=organization_metadata,
            repository_statistics=repository_statistics,
            technology_profile=technologies,
            activity_summary=activity_summary,
            ecosystem_indicators=ecosystem_indicators,
        )

    @staticmethod
    def _technology_profile(repositories: list[Mapping[str, Any]]) -> list[str]:
        """Return unique languages and topics across repository metadata."""

        technologies: list[str] = []
        for repository in repositories:
            values = [repository.get("language"), *repository.get("topics", [])]
            for value in values:
                if isinstance(value, str) and value and value not in technologies:
                    technologies.append(value)
        return technologies

    @staticmethod
    def _integer(value: object) -> int:
        """Convert API counts safely."""

        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _latest_update(repositories: list[Mapping[str, Any]]) -> str | None:
        """Return the latest repository update timestamp."""

        updates = [
            value
            for repository in repositories
            if isinstance((value := repository.get("updated_at")), str)
        ]
        return max(updates) if updates else None
