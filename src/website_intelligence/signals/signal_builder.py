import hashlib
from dataclasses import dataclass

from src.core_intelligence.models import Signal
from src.website_intelligence.analysis import AnalysisOutput


@dataclass(frozen=True, slots=True)
class SignalRule:
    signal_type: str
    finding_types: tuple[str, ...]
    assessment_types: tuple[str, ...]
    severity: str
    recommendation: str
    require_all_assessments: bool = True
    minimum_confidence: float = 0.6


class SignalBuilder:
    """Build explainable canonical signals from Website analysis output."""

    def build(self, output: AnalysisOutput, rule: SignalRule) -> Signal | None:
        findings = tuple(item for item in output.findings if item.finding_type in rule.finding_types)
        assessments = tuple(item for item in output.assessments if item.assessment_type in rule.assessment_types)
        names = {item.assessment_type for item in assessments}
        required = set(rule.assessment_types)
        satisfied = required.issubset(names) if rule.require_all_assessments else bool(required & names)
        if not findings or not satisfied:
            return None
        evidence = tuple(dict.fromkeys(ref for item in (*findings, *assessments) for ref in (item.supporting_evidence if hasattr(item, "supporting_evidence") else item.evidence)))
        confidence = round(min(sum(item.confidence for item in findings + assessments) / len(findings + assessments), 1.0), 4)
        if confidence < rule.minimum_confidence or not evidence:
            return None
        digest = hashlib.sha256(f"{output.observation.observation_id}:{rule.signal_type}:{evidence}".encode()).hexdigest()[:16]
        return Signal(f"website:signal:{digest}", output.observation.source_identifier, rule.signal_type, rule.severity, confidence, rule.recommendation, f"{rule.signal_type} supported by findings {', '.join(item.finding_type for item in findings)} and assessments {', '.join(item.assessment_type for item in assessments)}.", evidence, output.observation.observed_at)
