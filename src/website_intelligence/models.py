"""Immutable source-domain contracts for Website Intelligence."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Website:
    website_id: str
    url: str
    domain: str
    name: str | None = None
    description: str | None = None


@dataclass(frozen=True, slots=True)
class Page:
    page_id: str
    website_id: str
    url: str
    title: str | None = None
    description: str | None = None
    published_at: datetime | None = None
    modified_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class Link:
    link_id: str
    source_page_id: str
    target_url: str
    text: str | None = None
    relationship: str | None = None


@dataclass(frozen=True, slots=True)
class Document:
    document_id: str
    website_id: str
    url: str
    document_type: str
    title: str | None = None
    published_at: datetime | None = None
    modified_at: datetime | None = None
