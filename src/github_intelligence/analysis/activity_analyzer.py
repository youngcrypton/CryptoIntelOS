"""Repository activity metric extraction."""

from collections.abc import Mapping
from datetime import datetime, timezone
from typing import Any

from ..models import Repository


class ActivityAnalyzer:
    """Produce basic repository activity and popularity metrics."""

    def analyze(
        self,
        repository: Repository,
        metadata: Mapping[str, Any] | None = None,
    ) -> dict[str, int | float | str | None]:
        """Return age, popularity, issue, and update metrics."""

        source = metadata or {}
        created_at = source.get("created_at", repository.created_at)
        return {
            "repository_age_days": self._age_in_days(created_at),
            "stars": self._integer(source.get("stargazers_count", 0)),
            "forks": self._integer(source.get("forks_count", 0)),
            "watchers": self._integer(source.get("watchers_count", 0)),
            "open_issues": self._integer(source.get("open_issues_count", 0)),
            "last_updated": source.get("updated_at", repository.updated_at),
        }

    @staticmethod
    def _integer(value: object) -> int:
        """Convert a numeric API value to an integer safely."""

        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _age_in_days(created_at: object) -> int | None:
        """Calculate repository age from an ISO timestamp."""

        if not isinstance(created_at, str):
            return None
        try:
            created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        except ValueError:
            return None
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        return max(0, (datetime.now(timezone.utc) - created).days)
