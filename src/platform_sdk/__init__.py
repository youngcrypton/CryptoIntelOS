"""Internal source-integration contracts for CryptoIntel OS."""

from .adapter import SourceAdapter
from .collector import SourceCollector
from .lifecycle import CANONICAL_LIFECYCLE, LifecycleStage
from .metadata import IntegrationMetadata
from .pipeline import IntegrationPipeline
from .runtime import RuntimeFacade
from .translator import (
    AssessmentTranslator,
    EvidenceTranslator,
    FindingTranslator,
    ObservationTranslator,
)
from .validation import (
    AssessmentValidator,
    EvidenceValidator,
    FindingValidator,
    ObservationValidator,
    SignalValidator,
    ValidationResult,
)

__all__ = (
    "AssessmentTranslator",
    "AssessmentValidator",
    "CANONICAL_LIFECYCLE",
    "EvidenceTranslator",
    "EvidenceValidator",
    "FindingTranslator",
    "FindingValidator",
    "IntegrationMetadata",
    "IntegrationPipeline",
    "LifecycleStage",
    "ObservationTranslator",
    "ObservationValidator",
    "RuntimeFacade",
    "SignalValidator",
    "SourceAdapter",
    "SourceCollector",
    "ValidationResult",
)
