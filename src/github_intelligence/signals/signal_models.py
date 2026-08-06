"""Data models for GitHub intelligence signals."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SignalEvidence:
    """One observable fact supporting an intelligence signal."""

    source: str
    detail: str


@dataclass(frozen=True)
class IntelligenceSignal:
    """A named signal with confidence and supporting evidence."""

    name: str
    confidence: float
    evidence: list[SignalEvidence]


@dataclass(frozen=True)
class SignalReport:
    """Collection of generated signals and aggregated evidence summaries."""

    generated_signals: list[IntelligenceSignal]
    confidence_summary: dict[str, float]
    evidence_summary: list[SignalEvidence]
    generation_timestamp: datetime
