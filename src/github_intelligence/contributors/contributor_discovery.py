"""Contributor request preparation and response conversion."""

import json
from collections.abc import Mapping
from urllib.parse import urlencode
from urllib.request import Request

from ..client import GitHubClient
from ..models import Contributor


class ContributorDiscovery:
    """Prepare contributor and user-metadata requests without commit analysis."""

    def __init__(self, client: GitHubClient) -> None:
        """Initialize discovery with a reusable GitHub client."""

        self.client = client

    def prepare_repository_contributors_request(
        self,
        owner: str,
        repository: str,
        page: int = 1,
        per_page: int = 30,
    ) -> Request:
        """Prepare one paginated repository-contributors request."""

        return self._prepare_paginated_request(
            f"/repos/{self._part(owner)}/{self._part(repository)}/contributors",
            page,
            per_page,
        )

    def prepare_contributor_metadata_request(self, login: str) -> Request:
        """Prepare a request for public contributor metadata."""

        return self.client.prepare_request(f"/users/{self._part(login)}")

    def prepare_commit_analysis_request(
        self,
        owner: str,
        repository: str,
        login: str,
        page: int = 1,
        per_page: int = 30,
    ) -> Request:
        """Prepare a future commit-analysis request without executing it."""

        path = f"/repos/{self._part(owner)}/{self._part(repository)}/commits"
        parameters = {"author": self._part(login)}
        request = self._prepare_paginated_request(path, page, per_page, parameters)
        return request

    @staticmethod
    def contributors_from_response(
        response_payload: list[object] | Mapping[str, object] | str,
    ) -> list[Contributor]:
        """Convert a contributor-list response into shared contributor models."""

        payload = ContributorDiscovery._decode(response_payload)
        items = payload if isinstance(payload, list) else payload.get("items", [])
        if not isinstance(items, list):
            return []
        return [
            Contributor(
                login=str(item.get("login", "")),
                id=int(item.get("id", 0)),
                contributions=int(item.get("contributions", 0) or 0),
                avatar_url=item.get("avatar_url"),
                html_url=item.get("html_url"),
            )
            for item in items
            if isinstance(item, Mapping)
        ]

    def _prepare_paginated_request(
        self,
        path: str,
        page: int,
        per_page: int,
        extra_parameters: Mapping[str, str] | None = None,
    ) -> Request:
        """Prepare a validated paginated GitHub request."""

        if page < 1 or per_page < 1:
            raise ValueError("page and per_page must be positive")
        parameters: dict[str, int | str] = {"page": page, "per_page": per_page}
        if extra_parameters:
            parameters.update(extra_parameters)
        return self.client.prepare_request(f"{path}?{urlencode(parameters)}")

    @staticmethod
    def _part(value: str) -> str:
        """Validate and normalize one URL path component."""

        normalized = value.strip()
        if not normalized:
            raise ValueError("path components must not be empty")
        return normalized

    @staticmethod
    def _decode(
        response_payload: list[object] | Mapping[str, object] | str,
    ) -> list[object] | Mapping[str, object]:
        """Decode a list, mapping, or JSON response body."""

        if isinstance(response_payload, str):
            return json.loads(response_payload)
        return response_payload
