class ProjectProfileError(Exception):
    """Base error for unified project profile composition."""


class DuplicateProfileStrategyError(ProjectProfileError):
    """Raised when a profile strategy is registered twice."""


class ProfileStrategyNotFoundError(ProjectProfileError):
    """Raised when a profile strategy is unavailable."""
