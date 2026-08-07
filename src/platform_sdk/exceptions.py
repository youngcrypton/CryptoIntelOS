class PlatformSDKError(Exception):
    """Base error for SDK contract failures."""


class IntegrationConfigurationError(PlatformSDKError):
    """Raised when an integration contract is configured incorrectly."""
