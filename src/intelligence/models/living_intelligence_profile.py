"""
Living Intelligence Profile

Defines the central intelligence object used throughout CryptoIntel OS.

Every autonomous engine enriches this profile. It becomes the single
source of truth for everything known about a discovered project.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from src.intelligence.models.analyzer_result import AnalyzerResult


@dataclass
class LivingIntelligenceProfile:
    """
    Central intelligence object for a discovered project.
    """

    # ==========================================================
    # Core Identity
    # ==========================================================

    repository: Dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Discovery
    # ==========================================================

    discovery_evidence: List[Dict[str, Any]] = field(default_factory=list)
    discovery_history: List[Dict[str, Any]] = field(default_factory=list)

    # ==========================================================
    # Repository Intelligence
    # ==========================================================

    metadata: Dict[str, Any] = field(default_factory=dict)
    documentation: Dict[str, Any] = field(default_factory=dict)
    technology: Dict[str, Any] = field(default_factory=dict)
    activity: Dict[str, Any] = field(default_factory=dict)
    community: Dict[str, Any] = field(default_factory=dict)
    ecosystem: Dict[str, Any] = field(default_factory=dict)
    security: Dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # AI Intelligence
    # ==========================================================

    ai_findings: List[Dict[str, Any]] = field(default_factory=list)
    ai_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    ai_decisions: List[Dict[str, Any]] = field(default_factory=list)

    # ==========================================================
    # Scores
    # ==========================================================

    scores: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0

    # ==========================================================
    # Monitoring
    # ==========================================================

    monitoring: Dict[str, Any] = field(default_factory=dict)

    # ==========================================================
    # Distribution
    # ==========================================================

    distribution_history: List[Dict[str, Any]] = field(default_factory=list)

    # ==========================================================
    # Intelligence Merge
    # ==========================================================

    def merge(self, result: AnalyzerResult) -> None:
        """
        Merge an AnalyzerResult into the appropriate profile section.
        """

        if not result.success:
            return

        if not hasattr(self, result.section):
            raise AttributeError(
                f"LivingIntelligenceProfile has no section "
                f"'{result.section}'"
            )

        target = getattr(self, result.section)

        if isinstance(target, dict):
            target.update(result.data)

        elif isinstance(target, list):
            target.extend(result.data)

        else:
            raise TypeError(
                f"Unsupported profile section type: {result.section}"
            )

    # ==========================================================
    # Serialization
    # ==========================================================

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the intelligence profile into a serializable dictionary.
        """

        return {
            "repository": self.repository,
            "discovery_evidence": self.discovery_evidence,
            "discovery_history": self.discovery_history,
            "metadata": self.metadata,
            "documentation": self.documentation,
            "technology": self.technology,
            "activity": self.activity,
            "community": self.community,
            "ecosystem": self.ecosystem,
            "security": self.security,
            "ai_findings": self.ai_findings,
            "ai_recommendations": self.ai_recommendations,
            "ai_decisions": self.ai_decisions,
            "scores": self.scores,
            "confidence": self.confidence,
            "monitoring": self.monitoring,
            "distribution_history": self.distribution_history,
        }