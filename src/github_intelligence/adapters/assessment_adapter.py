from datetime import UTC, datetime

from src.core_intelligence.models import Assessment
from src.github_intelligence.repository_scoring import RepositoryScore


class RepositoryAssessmentAdapter:
    """Translate GitHub scoring output into a canonical Assessment."""

    def to_assessment(
        self,
        score: RepositoryScore,
        *,
        evidence: tuple[str, ...],
        entity_reference: str,
    ) -> Assessment:
        return Assessment(
            assessment_id=f"github:assessment:{entity_reference}",
            entity_reference=entity_reference,
            assessment_type="repository_quality",
            score=score.overall_repository_score,
            confidence=score.confidence_score,
            evidence=evidence or (entity_reference,),
            policy_name="github_repository_scoring",
            policy_version="1.0",
            generated_at=datetime.now(UTC),
        )
