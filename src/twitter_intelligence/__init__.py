"""Twitter Intelligence foundation built on the Platform Integration SDK."""

from .adapter import TwitterPostAdapter, TwitterProfileAdapter
from .collector import TwitterCollector
from .metadata import TWITTER_INTEGRATION_METADATA
from .models import TwitterPost, TwitterProfile
from .runtime import TwitterRuntimeIntegration

__all__ = (
    "TWITTER_INTEGRATION_METADATA",
    "TwitterCollector",
    "TwitterPost",
    "TwitterPostAdapter",
    "TwitterProfile",
    "TwitterProfileAdapter",
    "TwitterRuntimeIntegration",
)
