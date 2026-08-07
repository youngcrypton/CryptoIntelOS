from typing import Protocol

from src.platform_sdk import SourceAdapter

from .models import Document, Link, Page, Website


class WebsiteAdapter(SourceAdapter[Website], Protocol):
    """Translate website records into canonical observations."""


class PageAdapter(SourceAdapter[Page], Protocol):
    """Translate page records into canonical observations."""


class LinkAdapter(SourceAdapter[Link], Protocol):
    """Translate link records into canonical observations."""


class DocumentAdapter(SourceAdapter[Document], Protocol):
    """Translate document records into canonical observations."""
