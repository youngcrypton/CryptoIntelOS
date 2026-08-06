"""Common GitHub metadata models."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Repository:
    """Common repository metadata."""

    id: int
    name: str
    full_name: str
    html_url: str | None = None
    description: str | None = None
    private: bool = False
    default_branch: str | None = None
    owner_login: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


@dataclass(frozen=True)
class Organization:
    """Common organization metadata."""

    id: int
    login: str
    name: str | None = None
    html_url: str | None = None
    description: str | None = None
    avatar_url: str | None = None


@dataclass(frozen=True)
class Contributor:
    """Common contributor metadata."""

    login: str
    id: int
    contributions: int = 0
    avatar_url: str | None = None
    html_url: str | None = None


@dataclass(frozen=True)
class Commit:
    """Common commit metadata."""

    sha: str
    message: str
    author_login: str | None = None
    author_name: str | None = None
    authored_at: str | None = None
    html_url: str | None = None


@dataclass(frozen=True)
class Release:
    """Common release metadata."""

    id: int
    tag_name: str
    name: str | None = None
    body: str | None = None
    prerelease: bool = False
    draft: bool = False
    published_at: str | None = None
    html_url: str | None = None
