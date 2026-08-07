import hashlib
from dataclasses import dataclass

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation
from src.runtime.engine import ExecutionContext, ExecutionResult

from ..runtime import TwitterRuntimeIntegration
from .assessment_builder import AssessmentBuilder


RULES = (
    ("founder", "Founder identity", ("founder", "ceo", "co-founder"), "Active Founder", "Founder Credibility"),
    ("organization", "Organization identity", ("official", "protocol", "labs", "network"), "Organization Activity", "Team Visibility"),
    ("developer", "Developer activity", ("github", "shipped", "release", "build", "mainnet"), "Active Development Team", "Product Maturity"),
    ("hiring", "Hiring activity", ("hiring", "we're hiring", "join our team", "job opening"), "Hiring Activity", "Team Visibility"),
    ("funding", "Funding mention", ("raised", "funding", "investment", "invested", "seed round"), "Funding Activity", "Funding Confidence"),
    ("partnership", "Partnership mention", ("partner", "partnership", "integrat", "collaborat"), "Partnership Activity", "Partnership Confidence"),
    ("product", "Product release", ("launch", "release", "beta", "testnet", "mainnet", "product"), "Product Shipping", "Product Maturity"),
    ("ecosystem", "Ecosystem participation", ("ecosystem", "chain", "protocol", "defi", "web3"), "Ecosystem Expansion", "Ecosystem Presence"),
    ("narrative", "Narrative participation", ("ai", "defi", "rwa", "gaming", "restaking", "privacy"), "Emerging Narrative", "Narrative Strength"),
    ("community", "Community engagement", ("community", "users", "community call", "ama", "discord", "telegram"), "Strong Community", "Community Health"),
)


@dataclass(frozen=True, slots=True)
class AnalysisOutput:
    observation: Observation
    evidence: tuple[Evidence, ...]
    findings: tuple[Finding, ...]
    assessments: tuple[Assessment, ...]


class TwitterAnalysisEngine:
    """Apply deterministic keyword rules to Twitter observations."""

    def analyze(self, observation: Observation) -> AnalysisOutput:
        text = str(observation.raw_payload.get("text", "")) if isinstance(observation.raw_payload, dict) else str(observation.raw_payload)
        lowered = text.casefold()
        evidence: list[Evidence] = []
        findings: list[Finding] = []
        for key, label, terms, finding_type, _assessment_type in RULES:
            matches = tuple(term for term in terms if term in lowered)
            if not matches:
                continue
            evidence_id = self._id("evidence", observation.observation_id, key)
            evidence.append(Evidence(evidence_id, observation.source_identifier, observation.observation_id, f"twitter.{key}", {"matches": matches, "description": label}, min(1.0, .5 + .1 * len(matches)), "twitter", {"terms": matches}, observation.observed_at))
            finding_id = self._id("finding", observation.observation_id, key)
            findings.append(Finding(finding_id, observation.source_identifier, finding_type, evidence[-1].confidence, (evidence_id,), f"{label} detected from: {', '.join(matches)}", observation.observed_at))
        if not any(item.metric in {"twitter.developer", "twitter.product"} for item in evidence):
            evidence_id = self._id("evidence", observation.observation_id, "dormant")
            evidence.append(Evidence(evidence_id, observation.source_identifier, observation.observation_id, "twitter.developer", {"status": "no activity terms"}, .5, "twitter", {"rule": "absence-of-activity-terms"}, observation.observed_at))
            findings.append(Finding(self._id("finding", observation.observation_id, "dormant"), observation.source_identifier, "Dormant Activity", .5, (evidence_id,), "No developer or product activity terms were present in the observation", observation.observed_at))
        assessments = AssessmentBuilder().build(
            observation, tuple(evidence), tuple(findings)
        )
        return AnalysisOutput(observation, tuple(evidence), tuple(findings), assessments)

    @staticmethod
    def _id(kind: str, observation_id: str, key: str) -> str:
        digest = hashlib.sha256(f"{kind}:{observation_id}:{key}".encode()).hexdigest()[:16]
        return f"twitter:{kind}:{digest}"

    @staticmethod
    def enter_runtime(output: AnalysisOutput, integration: TwitterRuntimeIntegration, context: ExecutionContext) -> ExecutionResult:
        return integration.integrate((output.observation, output.evidence, output.findings, output.assessments, ()), context)
