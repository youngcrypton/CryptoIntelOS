class WebsiteIntelligenceError(Exception):
    """Base error for Website Intelligence foundation contracts."""


class WebsiteCollectionError(WebsiteIntelligenceError):
    """Raised by future website collection implementations."""


class WebsiteAdapterError(WebsiteIntelligenceError):
    """Raised by future website adapter implementations."""
