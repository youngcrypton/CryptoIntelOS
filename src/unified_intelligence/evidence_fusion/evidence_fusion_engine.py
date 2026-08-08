from collections import defaultdict

from src.core_intelligence.models import Evidence
from src.unified_intelligence.entity_linking import IdentityBundle

from .confidence import FusionConfidence
from .evidence_bundle import UnifiedEvidenceBundle
from .evidence_group import EvidenceGroup
from .evidence_reference import EvidenceReference
from .evidence_trace import EvidenceTrace
from .fusion_context import FusionContext
from .fusion_registry import FusionRegistry
from .fusion_result import FusionResult


class DeterministicEvidenceFusion:
    strategy_id = "deterministic-evidence-v1"

    def fuse(self, identity: IdentityBundle, evidence: tuple[Evidence, ...], context: FusionContext) -> FusionResult:
        groups: dict[tuple[str, str, str, str], list[Evidence]] = defaultdict(list)
        for item in evidence:
            key = (identity.canonical_project_identifier, item.source, item.metric, item.timestamp.isoformat())
            groups[key].append(item)
        result = []
        for (identity_id, source, evidence_type, timestamp), items in sorted(groups.items()):
            refs = tuple(EvidenceReference(item.evidence_id, item.source, item) for item in items)
            traces = tuple(EvidenceTrace(item.evidence_id, item.source, item.observation_reference, f"{identity_id}:{source}:{evidence_type}:{timestamp}") for item in items)
            result.append(EvidenceGroup(result_key := f"{identity_id}:{source}:{evidence_type}:{timestamp}", evidence_type, source, timestamp, refs, traces))
        groups_tuple = tuple(result)
        source_map = tuple((source, tuple(ref.evidence_id for group in groups_tuple if group.source == source for ref in group.references)) for source in sorted({group.source for group in groups_tuple}))
        provenance = tuple((ref.evidence_id, ref.evidence.source) for group in groups_tuple for ref in group.references)
        traceability = tuple(ref.evidence_id for group in groups_tuple for ref in group.references)
        confidence = FusionConfidence(1.0 if groups_tuple else 0.0, "explicit source evidence grouped without inference")
        return FusionResult(UnifiedEvidenceBundle(identity, groups_tuple, source_map, provenance, confidence, traceability))


class EvidenceFusionEngine:
    def __init__(self, registry: FusionRegistry | None = None) -> None:
        self.registry = registry or self.default_registry()

    @staticmethod
    def default_registry() -> FusionRegistry:
        registry = FusionRegistry()
        registry.register(DeterministicEvidenceFusion())
        return registry

    def fuse(self, identity: IdentityBundle, evidence: tuple[Evidence, ...], context: FusionContext) -> FusionResult:
        return self.registry.get("deterministic-evidence-v1").fuse(identity, evidence, context)
