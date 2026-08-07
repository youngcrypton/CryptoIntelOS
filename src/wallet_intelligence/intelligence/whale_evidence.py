from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WhaleEvidence:
    evidence_id: str
    metric: str
    value: float
    explanation: str
    source: str = "wallet_intelligence"
