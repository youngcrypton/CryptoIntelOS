from typing import Protocol

from src.platform_sdk import SourceCollector


class WebsiteCollector(SourceCollector, Protocol):
    """SDK collector contract for future website collection implementations."""
