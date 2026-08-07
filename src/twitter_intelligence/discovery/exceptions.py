class TwitterDiscoveryError(Exception):
    """Base error for deterministic Twitter discovery."""


class InvalidDiscoveryInputError(TwitterDiscoveryError):
    """Raised when supplied discovery input is structurally invalid."""
