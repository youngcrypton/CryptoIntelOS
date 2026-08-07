"""Website Intelligence foundation built on the Platform Integration SDK."""

from .adapter import DocumentAdapter, LinkAdapter, PageAdapter, WebsiteAdapter
from .collector import WebsiteCollector
from .metadata import WEBSITE_INTEGRATION_METADATA
from .models import Document, Link, Page, Website
from .runtime import WebsiteRuntimeIntegration
from .discovery import (
    DiscoveredEntity,
    DiscoveredEntityType,
    DiscoveryResult,
    WebsiteDiscoveryEngine,
)
from .analysis import AnalysisOutput, WebsiteAnalysisEngine
from .signals import SignalOutput, WebsiteSignalEngine
from .vertical_slice import WebsiteVerticalSlice, WebsiteVerticalSliceResult

__all__ = (
    "Document",
    "AnalysisOutput",
    "DocumentAdapter",
    "DiscoveredEntity",
    "DiscoveredEntityType",
    "DiscoveryResult",
    "Link",
    "LinkAdapter",
    "Page",
    "PageAdapter",
    "WEBSITE_INTEGRATION_METADATA",
    "Website",
    "WebsiteAdapter",
    "WebsiteAnalysisEngine",
    "WebsiteCollector",
    "WebsiteDiscoveryEngine",
    "WebsiteRuntimeIntegration",
    "SignalOutput",
    "WebsiteSignalEngine",
    "WebsiteVerticalSlice",
    "WebsiteVerticalSliceResult",
)
