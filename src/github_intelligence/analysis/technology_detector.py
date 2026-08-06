"""Technology detection from common GitHub repository metadata."""

from collections.abc import Mapping
from typing import Any

from ..models import Repository


class TechnologyDetector:
    """Identify declared languages and technology topics for a repository."""

    def detect(
        self,
        repository: Repository,
        metadata: Mapping[str, Any] | None = None,
    ) -> list[str]:
        """Return unique technologies inferred from metadata, preserving order."""

        source = metadata or {}
        technologies: list[str] = []
        self._append(technologies, source.get("language"))
        for topic in source.get("topics", []):
            self._append(technologies, topic)
        for classifier in source.get("classifiers", []):
            self._append(technologies, classifier)
        if not technologies and repository.default_branch:
            technologies.append(f"Git repository ({repository.default_branch})")
        return technologies

    @staticmethod
    def _append(values: list[str], value: object) -> None:
        """Append a non-empty value once."""

        if isinstance(value, str) and value.strip() and value not in values:
            values.append(value)
