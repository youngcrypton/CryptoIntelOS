class EntityLinkingError(Exception):
    """Base error for deterministic entity linking."""


class DuplicateLinkingStrategyError(EntityLinkingError):
    """Raised when a strategy identifier is registered twice."""


class LinkingStrategyNotFoundError(EntityLinkingError):
    """Raised when a linking strategy is unavailable."""
