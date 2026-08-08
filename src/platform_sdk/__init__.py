"""Internal source-integration contracts for CryptoIntel OS."""

from .adapter import SourceAdapter
from .collector import SourceCollector
from .lifecycle import CANONICAL_LIFECYCLE, LifecycleStage
from .metadata import IntegrationMetadata
from .pipeline import IntegrationPipeline
from .runtime import (
    CanonicalOutput,
    RuntimeFacade,
    UnsupportedRuntimeTypeError,
    execute_synchronously,
    flatten_canonical_output,
    validate_canonical_output,
    validate_execution_context,
)
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
    "CanonicalOutput",
    "UnsupportedRuntimeTypeError",
    "execute_synchronously",
    "flatten_canonical_output",
    "validate_canonical_output",
    "validate_execution_context",
    "SignalValidator",
    "SourceAdapter",
    "SourceCollector",
    "ValidationResult",
)
