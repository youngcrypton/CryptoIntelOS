class TwitterAnalysisError(Exception):
    """Base error for deterministic Twitter analysis."""


class InvalidAnalysisInputError(TwitterAnalysisError):
    """Raised when an observation cannot be analyzed."""
