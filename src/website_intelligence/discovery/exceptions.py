class WebsiteDiscoveryError(Exception):
    """Base error for deterministic website discovery."""


class InvalidDiscoveryInputError(WebsiteDiscoveryError):
    """Raised when supplied website discovery input is invalid."""
