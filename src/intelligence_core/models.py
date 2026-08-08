"""Deprecated pre-Kernel intelligence models.

Use ``src.core_intelligence.models.Signal`` and the Unified project profile.
"""

__deprecated__ = True

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .confidence import ConfidenceScore
from .enums import IntelligenceSource, MonitoringPriority, SignalSeverity
from .evidence import IntelligenceEvidence
from .priority import priority_for_severity


@dataclass(frozen=True)
class LegacyIntelligenceSignal:
    """Source-agnostic signal composed of confidence and traceable evidence."""

    name: str
    summary: str
    severity: SignalSeverity
    confidence: ConfidenceScore
    evidence: list[IntelligenceEvidence] = field(default_factory=list)
    source: IntelligenceSource | str = IntelligenceSource.UNKNOWN
    priority: MonitoringPriority | None = None

    def __post_init__(self) -> None:
        """Set a severity-derived priority when one is not supplied."""

        if self.priority is None:
            object.__setattr__(self, "priority", priority_for_severity(self.severity))


@dataclass(frozen=True)
class LegacyIntelligenceProfile:
    """Collection of signals and metadata for any monitored subject."""

    subject: str
    signals: list[IntelligenceSignal] = field(default_factory=list)
    sources: list[IntelligenceSource | str] = field(default_factory=list)
    generated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    metadata: dict[str, object] = field(default_factory=dict)


IntelligenceSignal = LegacyIntelligenceSignal
IntelligenceProfile = LegacyIntelligenceProfile
