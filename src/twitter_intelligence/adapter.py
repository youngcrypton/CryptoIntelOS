from typing import Protocol

from src.platform_sdk import SourceAdapter

from .models import TwitterPost, TwitterProfile


class TwitterPostAdapter(SourceAdapter[TwitterPost], Protocol):
    """Translate Twitter posts into canonical observations."""


class TwitterProfileAdapter(SourceAdapter[TwitterProfile], Protocol):
    """Translate Twitter profiles into canonical observations."""
