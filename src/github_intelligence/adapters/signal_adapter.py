from src.core_intelligence.models import Signal
from src.github_intelligence.signal_engine import GitHubIntelligenceSignal


class GitHubSignalAdapter:
    """Translate explainable GitHub signals to the canonical Signal contract."""

    def to_signal(self, value: GitHubIntelligenceSignal, *, entity_reference: str) -> Signal:
        return Signal(
            signal_id=value.signal_id,
            entity_reference=entity_reference,
            signal_type=value.category,
            severity=value.severity,
            confidence=value.confidence,
            recommendation=value.signal_name,
            explanation=value.explanation,
            supporting_evidence=value.supporting_evidence or (value.signal_id,),
            timestamp=value.timestamp,
        )
