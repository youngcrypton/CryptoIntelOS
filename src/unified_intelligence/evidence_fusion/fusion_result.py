from dataclasses import dataclass

from .evidence_bundle import UnifiedEvidenceBundle


@dataclass(frozen=True, slots=True)
class FusionResult:
    bundle: UnifiedEvidenceBundle
