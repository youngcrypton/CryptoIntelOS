"""Organization request preparation and response conversion."""

import json
from collections.abc import Mapping
from urllib.parse import urlencode
from urllib.request import Request

from ..client import GitHubClient
from ..models import Organization, Repository


class OrganizationDiscovery:
    """Prepare organization metadata, repository, and member requests."""

    def __init__(self, client: GitHubClient) -> None:
        """Initialize discovery with a reusable GitHub client."""

        self.client = client

    def prepare_metadata_request(self, login: str) -> Request:
        """Prepare a request for organization metadata."""

        return self.client.prepare_request(f"/orgs/{self._login(login)}")

    def prepare_repositories_request(
        self,
        login: str,
        page: int = 1,
        per_page: int = 30,
    ) -> Request:
        """Prepare one paginated organization-repositories request."""

        return self._prepare_paginated_request(
            f"/orgs/{self._login(login)}/repos",
            page,
            per_page,
        )

    def prepare_members_request(
        self,
        login: str,
        page: int = 1,
        per_page: int = 30,
    ) -> Request:
        """Prepare one paginated organization-members request for future use."""

        return self._prepare_paginated_request(
            f"/orgs/{self._login(login)}/members",
            page,
            per_page,
        )

    @staticmethod
    def organization_from_response(
        response_payload: Mapping[str, object] | str,
    ) -> Organization:
        """Convert an organization response payload to the shared model."""

        payload = OrganizationDiscovery._decode(response_payload)
        return Organization(
            id=int(payload.get("id", 0)),
            login=str(payload.get("login", "")),
            name=payload.get("name"),
            html_url=payload.get("html_url"),
            description=payload.get("description"),
            avatar_url=payload.get("avatar_url"),
        )

    @staticmethod
    def repositories_from_response(
        response_payload: Mapping[str, object] | str,
    ) -> list[Repository]:
        """Convert an organization repository-list payload to repository models."""

        payload = OrganizationDiscovery._decode(response_payload)
        items = payload if isinstance(payload, list) else payload.get("items", [])
        if not isinstance(items, list):
            return []
        return [
            Repository(
                id=int(item.get("id", 0)),
                name=str(item.get("name", "")),
                full_name=str(item.get("full_name", "")),
                html_url=item.get("html_url"),
                description=item.get("description"),
                private=bool(item.get("private", False)),
                default_branch=item.get("default_branch"),
                owner_login=(
                    item.get("owner", {}).get("login")
                    if isinstance(item.get("owner"), Mapping)
                    else None
                ),
                created_at=item.get("created_at"),
                updated_at=item.get("updated_at"),
            )
            for item in items
            if isinstance(item, Mapping)
        ]

    @staticmethod
    def _login(login: str) -> str:
        """Validate and normalize an organization login."""

        normalized_login = login.strip()
        if not normalized_login:
            raise ValueError("organization login must not be empty")
        return normalized_login

    def _prepare_paginated_request(
        self,
        path: str,
        page: int,
        per_page: int,
    ) -> Request:
        """Prepare a validated paginated request."""

        if page < 1 or per_page < 1:
            raise ValueError("page and per_page must be positive")
        return self.client.prepare_request(
            f"{path}?{urlencode({'page': page, 'per_page': per_page})}"
        )

    @staticmethod
    def _decode(response_payload: Mapping[str, object] | str) -> Mapping[str, object] | list[object]:
        """Decode a mapping or JSON response body."""

        if isinstance(response_payload, str):
            return json.loads(response_payload)
        return response_payload
