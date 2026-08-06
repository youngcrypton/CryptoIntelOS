"""Contributor profile data model."""

from dataclasses import dataclass

from ..models import Contributor


@dataclass(frozen=True)
class ContributorProfile:
    """Structured contributor metadata and repository involvement profile."""

    contributor: Contributor
    contributor_metadata: dict[str, object]
    contribution_summary: dict[str, int | float | str | None]
    repository_involvement: list[str]
    organization_affiliations: list[str]
    activity_summary: dict[str, int | float | str | None]
    technology_footprint: list[str]
