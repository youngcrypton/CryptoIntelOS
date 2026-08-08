class EvidenceFusionError(Exception):
    """Base error for deterministic evidence fusion."""


class DuplicateFusionStrategyError(EvidenceFusionError):
    """Raised when a fusion strategy is registered twice."""


class FusionStrategyNotFoundError(EvidenceFusionError):
    """Raised when a fusion strategy is unavailable."""
