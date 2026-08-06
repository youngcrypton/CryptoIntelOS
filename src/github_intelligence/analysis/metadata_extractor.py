"""Common metadata extraction for GitHub repositories."""

from collections.abc import Mapping
from typing import Any

from ..models import Repository


class MetadataExtractor:
    """Extract descriptive and repository configuration metadata."""

    def extract(
        self,
        repository: Repository,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, object]:
        """Return normalized metadata with model values as fallbacks."""

        source = metadata or {}
        license_data = source.get("license")
        license_name = self._license_name(license_data)
        owner_visibility = source.get("visibility")
        return {
            "description": source.get("description", repository.description),
            "homepage": source.get("homepage"),
            "topics": list(source.get("topics", [])),
            "license": license_name,
            "visibility": owner_visibility or ("private" if repository.private else "public"),
            "default_branch": source.get("default_branch", repository.default_branch),
            "repository_size": source.get("size"),
        }

    @staticmethod
    def _license_name(value: object) -> str | None:
        """Extract a license identifier or name from GitHub metadata."""

        if isinstance(value, Mapping):
            identifier = value.get("spdx_id") or value.get("key") or value.get("name")
            return str(identifier) if identifier else None
        return str(value) if isinstance(value, str) else None
