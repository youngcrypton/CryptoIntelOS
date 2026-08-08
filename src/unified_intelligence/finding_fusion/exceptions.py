class FindingFusionError(Exception):
    """Base error for deterministic finding fusion."""


class DuplicateFusionStrategyError(FindingFusionError):
    """Raised when a finding strategy is registered twice."""


class FusionStrategyNotFoundError(FindingFusionError):
    """Raised when a finding strategy is unavailable."""
