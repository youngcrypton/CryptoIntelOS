class BlockchainAdapterSDKError(Exception):
    """Base error for Blockchain Adapter SDK contracts."""


class DuplicateProviderError(BlockchainAdapterSDKError):
    """Raised when a provider identifier is registered twice."""


class ProviderNotFoundError(BlockchainAdapterSDKError):
    """Raised when a provider identifier is not registered."""


class DuplicateAdapterError(BlockchainAdapterSDKError):
    """Raised when an adapter identifier is registered twice."""


class AdapterNotFoundError(BlockchainAdapterSDKError):
    """Raised when an adapter identifier is not registered."""
