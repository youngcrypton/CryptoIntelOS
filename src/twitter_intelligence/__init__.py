"""Twitter Intelligence foundation built on the Platform Integration SDK."""

from .adapter import TwitterPostAdapter, TwitterProfileAdapter
from .collector import TwitterCollector
from .metadata import TWITTER_INTEGRATION_METADATA
from .models import TwitterPost, TwitterProfile
from .runtime import TwitterRuntimeIntegration
from .discovery import (
    DiscoveredEntity,
    DiscoveredEntityType,
    DiscoveryResult,
    TwitterDiscoveryEngine,
)
from .analysis import AnalysisOutput, TwitterAnalysisEngine
from .signals import SignalOutput, TwitterSignalEngine

__all__ = (
    "TWITTER_INTEGRATION_METADATA",
    "DiscoveredEntity",
    "DiscoveredEntityType",
    "DiscoveryResult",
    "AnalysisOutput",
    "SignalOutput",
    "TwitterCollector",
    "TwitterPost",
    "TwitterPostAdapter",
    "TwitterProfile",
    "TwitterProfileAdapter",
    "TwitterRuntimeIntegration",
    "TwitterDiscoveryEngine",
    "TwitterAnalysisEngine",
    "TwitterSignalEngine",
)
