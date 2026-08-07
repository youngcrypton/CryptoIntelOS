"""Website Intelligence foundation built on the Platform Integration SDK."""

from .adapter import DocumentAdapter, LinkAdapter, PageAdapter, WebsiteAdapter
from .collector import WebsiteCollector
from .metadata import WEBSITE_INTEGRATION_METADATA
from .models import Document, Link, Page, Website
from .runtime import WebsiteRuntimeIntegration

__all__ = (
    "Document",
    "DocumentAdapter",
    "Link",
    "LinkAdapter",
    "Page",
    "PageAdapter",
    "WEBSITE_INTEGRATION_METADATA",
    "Website",
    "WebsiteAdapter",
    "WebsiteCollector",
    "WebsiteRuntimeIntegration",
)
