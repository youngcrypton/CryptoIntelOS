class WebsiteAnalysisError(Exception):
    """Base error for deterministic Website analysis."""


class InvalidAnalysisInputError(WebsiteAnalysisError):
    """Raised when a canonical observation cannot be analyzed."""
