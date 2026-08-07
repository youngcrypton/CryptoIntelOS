class TwitterSignalError(Exception):
    """Base error for Twitter signal generation."""


class DuplicateSignalGeneratorError(TwitterSignalError):
    """Raised when a signal type is registered more than once."""
