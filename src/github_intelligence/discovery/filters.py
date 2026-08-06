"""Configurable filters for GitHub repository discovery results."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Mapping


@dataclass(frozen=True)
class RepositoryFilters:
    """Optional metadata constraints applied before model conversion."""

    minimum_stars: int | None = None
    language: str | None = None
    archived: bool | None = None
    fork: bool | None = None
    topics: tuple[str, ...] = field(default_factory=tuple)
    updated_after: str | datetime | None = None
    license: str | None = None

    def matches(self, repository_data: Mapping[str, Any]) -> bool:
        """Return whether a raw GitHub repository payload satisfies the filters."""

        if (
            self.minimum_stars is not None
            and int(repository_data.get("stargazers_count", 0)) < self.minimum_stars
        ):
            return False
        if self.language and repository_data.get("language") != self.language:
            return False
        if self.archived is not None and repository_data.get("archived") != self.archived:
            return False
        if self.fork is not None and repository_data.get("fork") != self.fork:
            return False
        if self.license and self._license_key(repository_data) != self.license:
            return False
        if self.topics and not set(self.topics).issubset(
            set(repository_data.get("topics", []))
        ):
            return False
        return self._updated_after_matches(repository_data.get("updated_at"))

    def _updated_after_matches(self, updated_at: object) -> bool:
        """Apply the optional ISO timestamp boundary."""

        if self.updated_after is None:
            return True
        if not isinstance(updated_at, str):
            return False

        boundary = self.updated_after
        boundary_text = (
            boundary.isoformat()
            if isinstance(boundary, datetime)
            else boundary
        )
        return updated_at > boundary_text

    @staticmethod
    def _license_key(repository_data: Mapping[str, Any]) -> str | None:
        """Read GitHub's nested license identifier from a raw payload."""

        license_data = repository_data.get("license")
        if isinstance(license_data, Mapping):
            key = license_data.get("spdx_id") or license_data.get("key")
            return str(key) if key else None
        return None
