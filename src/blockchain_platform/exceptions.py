class BlockchainPlatformError(Exception):
    """Base error for Blockchain Platform foundation contracts."""


class DuplicateBlockchainError(BlockchainPlatformError):
    """Raised when a chain identifier is registered more than once."""


class BlockchainNotFoundError(BlockchainPlatformError):
    """Raised when a requested chain is not registered."""
