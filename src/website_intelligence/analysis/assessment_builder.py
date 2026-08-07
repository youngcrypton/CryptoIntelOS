from src.core_intelligence.models import Assessment, Evidence, Finding, Observation


class AssessmentBuilder:
    """Build deterministic Website assessments from supported findings."""

    MAPPING = {
        "Identity Confidence": ("Verified Official Website",),
        "Documentation Quality": ("Strong Documentation", "Public Roadmap"),
        "Team Transparency": ("Transparent Team",),
        "Hiring Activity": ("Active Hiring",),
        "Security Maturity": ("Security Focus",),
        "Ecosystem Presence": ("Strong Ecosystem Presence",),
        "Communication Quality": ("Strong Communication",),
    }

    def build(self, observation: Observation, evidence: tuple[Evidence, ...], findings: tuple[Finding, ...]) -> tuple[Assessment, ...]:
        evidence_ids = {item.evidence_id for item in evidence}
        result = []
        for assessment_type, finding_types in self.MAPPING.items():
            relevant = tuple(item for item in findings if item.finding_type in finding_types)
            refs = tuple(dict.fromkeys(reference for item in relevant for reference in item.supporting_evidence))
            if not refs or not set(refs).issubset(evidence_ids):
                continue
            confidence = round(sum(item.confidence for item in relevant) / len(relevant), 4)
            result.append(Assessment(f"website:assessment:{observation.observation_id}:{assessment_type.casefold().replace(' ', '-')}", observation.source_identifier, assessment_type, round(confidence * 100, 2), confidence, refs, "website-deterministic", "1.0", observation.observed_at))
        return tuple(result)
