class WhaleIntelligenceError(Exception):
    """Base error for deterministic Whale Intelligence."""


class DuplicateWhaleError(WhaleIntelligenceError):
    """Raised when a whale profile is registered twice."""


class WhaleNotFoundError(WhaleIntelligenceError):
    """Raised when a whale profile is not registered."""
