from src.core_intelligence.models import Assessment, Evidence, Finding, Observation


class AssessmentBuilder:
    """Build deterministic normalized assessments from findings."""

    TYPES = ("Founder Credibility", "Team Visibility", "Community Health", "Ecosystem Presence", "Narrative Strength", "Partnership Confidence", "Funding Confidence", "Product Maturity")

    def build(self, observation: Observation, evidence: tuple[Evidence, ...], findings: tuple[Finding, ...]) -> tuple[Assessment, ...]:
        evidence_ids = {item.evidence_id for item in evidence}
        result = []
        for assessment_type in self.TYPES:
            relevant = [finding for finding in findings if self._matches(assessment_type, finding.finding_type)]
            refs = tuple(item.supporting_evidence[0] for item in relevant)
            if not refs or not set(refs).issubset(evidence_ids):
                continue
            score = round(sum(item.confidence for item in relevant) / len(relevant) * 100, 2)
            result.append(Assessment(f"twitter:assessment:{observation.observation_id}:{assessment_type.casefold().replace(' ', '-')}", observation.source_identifier, assessment_type, score, score / 100, refs, "twitter-deterministic", "1.0", observation.observed_at))
        return tuple(result)

    @staticmethod
    def _matches(assessment: str, finding: str) -> bool:
        mapping = {
            "Founder Credibility": ("Active Founder",),
            "Team Visibility": ("Hiring Activity", "Active Development Team", "Organization Activity"),
            "Community Health": ("Strong Community",),
            "Ecosystem Presence": ("Ecosystem Expansion",),
            "Narrative Strength": ("Emerging Narrative",),
            "Partnership Confidence": ("Partnership Activity",),
            "Funding Confidence": ("Funding Activity",),
            "Product Maturity": ("Product Shipping",),
        }
        return finding in mapping.get(assessment, ())
