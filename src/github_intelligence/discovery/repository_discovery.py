"""Repository search request preparation and response conversion."""

import json
from collections.abc import Iterable, Mapping
from urllib.parse import urlencode
from urllib.request import Request

from ..client import GitHubClient
from ..models import Repository
from .filters import RepositoryFilters


class RepositoryDiscovery:
    """Prepare paginated repository searches and convert filtered responses."""

    def __init__(
        self,
        client: GitHubClient,
        filters: RepositoryFilters | None = None,
    ) -> None:
        """Initialize discovery with a reusable client and optional filters."""

        self.client = client
        self.filters = filters or RepositoryFilters()

    def prepare_search_request(
        self,
        query: str,
        page: int = 1,
        per_page: int = 30,
    ) -> Request:
        """Prepare one authenticated, paginated repository search request."""

        if page < 1 or per_page < 1:
            raise ValueError("page and per_page must be positive")

        parameters = urlencode(
            {"q": query, "page": page, "per_page": per_page}
        )
        return self.client.prepare_request(f"/search/repositories?{parameters}")

    def prepare_search_requests(
        self,
        query: str,
        pages: int = 1,
        per_page: int = 30,
    ) -> list[Request]:
        """Prepare an ordered sequence of requests for paginated discovery."""

        if pages < 1:
            raise ValueError("pages must be positive")
        return [
            self.prepare_search_request(query, page, per_page)
            for page in range(1, pages + 1)
        ]

    def repositories_from_page(
        self,
        response_payload: Mapping[str, object] | str,
    ) -> list[Repository]:
        """Convert one API page payload into filtered repository models."""

        payload = self._decode_payload(response_payload)
        items = payload.get("items", [])
        if not isinstance(items, list):
            return []

        repositories: list[Repository] = []
        for item in items:
            if isinstance(item, Mapping) and self.filters.matches(item):
                repositories.append(self._to_repository(item))
        return repositories

    def repositories_from_pages(
        self,
        response_pages: Iterable[Mapping[str, object] | str],
    ) -> list[Repository]:
        """Convert multiple ordered API pages while preserving pagination order."""

        repositories: list[Repository] = []
        for response_page in response_pages:
            repositories.extend(self.repositories_from_page(response_page))
        return repositories

    @staticmethod
    def _decode_payload(
        response_payload: Mapping[str, object] | str,
    ) -> Mapping[str, object]:
        """Decode a mapping or JSON response body without making a request."""

        if isinstance(response_payload, str):
            decoded = json.loads(response_payload)
            if not isinstance(decoded, Mapping):
                raise ValueError("repository search response must be an object")
            return decoded
        return response_payload

    @staticmethod
    def _to_repository(repository_data: Mapping[str, object]) -> Repository:
        """Map common GitHub repository fields to the shared model."""

        owner = repository_data.get("owner")
        owner_login = owner.get("login") if isinstance(owner, Mapping) else None
        return Repository(
            id=int(repository_data.get("id", 0)),
            name=str(repository_data.get("name", "")),
            full_name=str(repository_data.get("full_name", "")),
            html_url=repository_data.get("html_url"),
            description=repository_data.get("description"),
            private=bool(repository_data.get("private", False)),
            default_branch=repository_data.get("default_branch"),
            owner_login=owner_login,
            created_at=repository_data.get("created_at"),
            updated_at=repository_data.get("updated_at"),
        )
