class AssessmentFusionError(Exception):
    """Base error for deterministic assessment fusion."""


class DuplicateFusionStrategyError(AssessmentFusionError):
    """Raised when an assessment strategy is registered twice."""


class FusionStrategyNotFoundError(AssessmentFusionError):
    """Raised when an assessment strategy is unavailable."""
