import hashlib
from dataclasses import dataclass

from src.core_intelligence.models import Signal
from src.twitter_intelligence.analysis import AnalysisOutput


@dataclass(frozen=True, slots=True)
class SignalRule:
    signal_type: str
    finding_types: tuple[str, ...]
    assessment_types: tuple[str, ...]
    severity: str
    recommendation: str
    require_all_assessments: bool = True


class SignalBuilder:
    """Build canonical signals from explicit findings and assessments."""

    def build(self, output: AnalysisOutput, rule: SignalRule) -> Signal | None:
        findings = tuple(
            item for item in output.findings if item.finding_type in rule.finding_types
        )
        assessments = tuple(
            item
            for item in output.assessments
            if item.assessment_type in rule.assessment_types
        )
        assessment_names = {item.assessment_type for item in assessments}
        required = set(rule.assessment_types)
        assessments_satisfied = (
            required.issubset(assessment_names)
            if rule.require_all_assessments
            else bool(required & assessment_names)
        )
        if not findings or not assessments_satisfied:
            return None
        evidence = tuple(
            dict.fromkeys(
                evidence_id
                for item in (*findings, *assessments)
                for evidence_id in (
                    item.supporting_evidence
                    if hasattr(item, "supporting_evidence")
                    else item.evidence
                )
            )
        )
        confidence = round(
            min(
                sum(item.confidence for item in findings + assessments)
                / len(findings + assessments),
                1.0,
            ),
            4,
        )
        if confidence < 0.6 or not evidence:
            return None
        explanation = (
            f"{rule.signal_type} supported by findings "
            f"{', '.join(item.finding_type for item in findings)} and assessments "
            f"{', '.join(item.assessment_type for item in assessments)}."
        )
        digest = hashlib.sha256(
            f"{output.observation.observation_id}:{rule.signal_type}:{evidence}".encode()
        ).hexdigest()[:16]
        return Signal(
            f"twitter:signal:{digest}",
            output.observation.source_identifier,
            rule.signal_type,
            rule.severity,
            confidence,
            rule.recommendation,
            explanation,
            evidence,
            output.observation.observed_at,
        )
