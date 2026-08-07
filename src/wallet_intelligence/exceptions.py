class WalletIntelligenceError(Exception):
    """Base error for wallet discovery and classification."""


class InvalidWalletInputError(WalletIntelligenceError):
    """Raised when a wallet cannot be classified from supplied data."""
