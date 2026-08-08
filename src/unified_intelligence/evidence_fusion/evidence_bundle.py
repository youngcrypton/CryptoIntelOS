from dataclasses import dataclass

from src.unified_intelligence.entity_linking import IdentityBundle

from .confidence import FusionConfidence
from .evidence_group import EvidenceGroup


@dataclass(frozen=True, slots=True)
class UnifiedEvidenceBundle:
    identity: IdentityBundle
    groups: tuple[EvidenceGroup, ...]
    source_map: tuple[tuple[str, tuple[str, ...]], ...]
    provenance: tuple[tuple[str, str], ...]
    confidence: FusionConfidence
    traceability: tuple[str, ...]
