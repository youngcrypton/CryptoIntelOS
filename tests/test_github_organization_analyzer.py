"""Tests for GitHub organization intelligence collection."""

import json
from collections.abc import Mapping
from typing import Any

import pytest

from src.github_intelligence import OrganizationAnalyzer


class FakeResponse:
    """Minimal context-managed HTTP response for analyzer tests."""

    def __init__(self, payload: object, headers: Mapping[str, str] | None = None) -> None:
        self._payload = payload
        self.headers = headers or {}

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


def test_analyze_collects_organization_intelligence() -> None:
    """Organization profile fields and public member counts are normalized."""

    metadata = {
        "id": 991,
        "login": "crypto-org",
        "name": "Crypto Org",
        "is_verified": True,
        "public_repos": 42,
        "followers": 1250,
        "following": 3,
        "description": "Building open crypto infrastructure.",
        "blog": "https://crypto.example",
        "location": "Lagos",
        "created_at": "2020-01-02T03:04:05Z",
        "updated_at": "2026-08-01T10:00:00Z",
        "html_url": "https://github.com/crypto-org",
        "avatar_url": "https://avatars.example/991",
        "email": "opensource@crypto.example",
        "twitter_username": "crypto_org",
    }
    responses = iter(
        [
            FakeResponse(metadata),
            FakeResponse(
                [{"login": "member-one"}],
                {
                    "Link": (
                        '<https://api.github.com/orgs/crypto-org/public_members'
                        '?per_page=1&page=17>; rel="last"'
                    )
                },
            ),
        ]
    )

    def opener(*args: Any, **kwargs: Any) -> FakeResponse:
        return next(responses)

    intelligence = OrganizationAnalyzer(opener=opener).analyze(" crypto-org ")

    assert intelligence.login == "crypto-org"
    assert intelligence.verified is True
    assert intelligence.repository_count == 42
    assert intelligence.public_member_count == 17
    assert intelligence.followers == 1250
    assert intelligence.following == 3
    assert intelligence.description == "Building open crypto infrastructure."
    assert intelligence.website == "https://crypto.example"
    assert intelligence.location == "Lagos"
    assert intelligence.created_at == "2020-01-02T03:04:05Z"
    assert intelligence.updated_at == "2026-08-01T10:00:00Z"


def test_analyze_counts_single_public_members_page() -> None:
    """A response without pagination reports the returned member count."""

    responses = iter(
        [
            FakeResponse({"id": 1, "login": "small-org"}),
            FakeResponse([{"login": "one"}]),
        ]
    )

    intelligence = OrganizationAnalyzer(
        opener=lambda *args, **kwargs: next(responses)
    ).analyze("small-org")

    assert intelligence.public_member_count == 1
    assert intelligence.repository_count == 0


def test_analyze_rejects_empty_login() -> None:
    """An organization login is required before making requests."""

    with pytest.raises(ValueError, match="organization login must not be empty"):
        OrganizationAnalyzer().analyze("   ")
