from typing import Protocol

from src.platform_sdk import SourceCollector


class TwitterCollector(SourceCollector, Protocol):
    """SDK collector contract for future Twitter collection implementations."""
