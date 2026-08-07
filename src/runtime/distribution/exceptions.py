class DistributionError(Exception):
    """Base error for distribution orchestration failures."""


class DistributionConfigurationError(DistributionError):
    """Raised when distribution contracts are configured incorrectly."""


class DistributionProviderNotFoundError(DistributionError):
    """Raised when a requested provider is not registered."""
