"""Organization profile data model."""

from dataclasses import dataclass

from ..models import Organization


@dataclass(frozen=True)
class OrganizationProfile:
    """Structured organization metadata, repository, technology, and activity data."""

    organization: Organization
    organization_metadata: dict[str, object]
    repository_statistics: dict[str, int | float]
    technology_profile: list[str]
    activity_summary: dict[str, int | float | str | None]
    ecosystem_indicators: list[str]
