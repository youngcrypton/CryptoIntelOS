class TwitterIntelligenceError(Exception):
    """Base error for Twitter Intelligence foundation contracts."""


class TwitterIntegrationConfigurationError(TwitterIntelligenceError):
    """Raised when Twitter SDK integration is configured incorrectly."""
