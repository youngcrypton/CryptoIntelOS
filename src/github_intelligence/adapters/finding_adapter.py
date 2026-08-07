from datetime import UTC, datetime

from src.core_intelligence.models import Finding
from src.github_intelligence.analysis.repository_analyzer import RepositoryAnalysis


class RepositoryFindingAdapter:
    """Translate repository analysis into an evidence-linked Finding."""

    def to_finding(
        self, analysis: RepositoryAnalysis, *, evidence: tuple[str, ...]
    ) -> Finding:
        return Finding(
            finding_id=f"github:finding:{analysis.repository.id}",
            entity_reference=f"github:repository:{analysis.repository.id}",
            finding_type="repository_analysis",
            confidence=1.0,
            supporting_evidence=evidence or (f"github:repository:{analysis.repository.id}",),
            explanation="GitHub repository analysis completed.",
            timestamp=datetime.now(UTC),
        )
