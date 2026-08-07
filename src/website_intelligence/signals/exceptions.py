class WebsiteSignalError(Exception):
    """Base error for Website signal generation."""


class DuplicateSignalGeneratorError(WebsiteSignalError):
    """Raised when a signal type is registered more than once."""
