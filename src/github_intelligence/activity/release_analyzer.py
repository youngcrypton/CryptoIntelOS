"""Release history metric analysis."""

import re
from collections.abc import Iterable
from datetime import datetime, timezone

from ..models import Release


class ReleaseAnalyzer:
    """Analyze release cadence, versioning, prereleases, and changelogs."""

    _SEMVER_PATTERN = re.compile(r"^v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")

    def analyze(self, releases: Iterable[Release]) -> dict[str, object]:
        """Return release metrics from supplied release models."""

        release_list = list(releases)
        dated_releases = sorted(
            release_list,
            key=lambda release: self._parse_timestamp(release.published_at)
            or datetime.min.replace(tzinfo=timezone.utc),
            reverse=True,
        )
        latest = dated_releases[0] if dated_releases else None
        return {
            "release_count": len(release_list),
            "release_frequency": len(release_list),
            "latest_release": latest.tag_name if latest else None,
            "semantic_versioning_usage": all(
                self._SEMVER_PATTERN.match(release.tag_name) is not None
                for release in release_list
            ) if release_list else False,
            "prerelease_count": sum(release.prerelease for release in release_list),
            "pre_release_detected": any(release.prerelease for release in release_list),
            "tagged_release_history": [release.tag_name for release in dated_releases],
            "changelog_available": any(
                bool(release.body and "changelog" in release.body.lower())
                for release in release_list
            ),
        }

    @staticmethod
    def _parse_timestamp(value: str | None) -> datetime | None:
        """Parse a release publication timestamp for ordering."""

        if not value:
            return None
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
