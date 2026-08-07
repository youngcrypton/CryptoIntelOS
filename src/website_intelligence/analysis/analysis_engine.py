import hashlib
import json
import re
from dataclasses import dataclass

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation
from src.runtime.engine import ExecutionContext, ExecutionResult

from ..runtime import WebsiteRuntimeIntegration
from .assessment_builder import AssessmentBuilder


@dataclass(frozen=True, slots=True)
class AnalysisRule:
    key: str
    evidence_label: str
    terms: tuple[str, ...]
    finding_type: str


RULES = (
    AnalysisRule("documentation", "Documentation availability", ("documentation", "docs", "gitbook"), "Strong Documentation"),
    AnalysisRule("whitepaper", "Whitepaper availability", ("whitepaper",), "Strong Documentation"),
    AnalysisRule("roadmap", "Roadmap availability", ("roadmap",), "Public Roadmap"),
    AnalysisRule("team", "Team transparency", ("team", "about-us", "leadership"), "Transparent Team"),
    AnalysisRule("careers", "Hiring evidence", ("careers", "jobs", "hiring"), "Active Hiring"),
    AnalysisRule("security", "Security evidence", ("audit", "audits", "security"), "Security Focus"),
    AnalysisRule("social", "Social presence", ("twitter.com", "x.com", "discord.gg", "t.me", "linkedin.com", "youtube.com", "medium.com"), "Strong Communication"),
    AnalysisRule("ecosystem", "Ecosystem participation", ("ecosystem", "ethereum", "solana", "defi", "web3", "protocol"), "Strong Ecosystem Presence"),
    AnalysisRule("contact", "Contact information", ("contact", "mailto:"), "Strong Communication"),
)


@dataclass(frozen=True, slots=True)
class AnalysisOutput:
    observation: Observation
    evidence: tuple[Evidence, ...]
    findings: tuple[Finding, ...]
    assessments: tuple[Assessment, ...]


class WebsiteAnalysisEngine:
    """Transform canonical Website observations with explicit deterministic rules."""

    def analyze(self, observation: Observation) -> AnalysisOutput:
        payload_text = json.dumps(observation.raw_payload, sort_keys=True, default=str).casefold()
        evidence: list[Evidence] = []
        findings: list[Finding] = []
        if observation.observation_id.startswith("website:website:"):
            self._append(observation, "identity", "Official website identity", ("website",), "Verified Official Website", evidence, findings)
        for rule in RULES:
            matches = tuple(term for term in rule.terms if term in payload_text)
            if matches:
                self._append(observation, rule.key, rule.evidence_label, matches, rule.finding_type, evidence, findings)
        emails = tuple(sorted(set(re.findall(r"[\w.+-]+@[\w.-]+\.[a-z]{2,}", payload_text))))
        if emails and not any(item.metric == "website.contact" for item in evidence):
            self._append(observation, "contact", "Contact information", emails, "Strong Communication", evidence, findings)
        if len(evidence) == 1 and evidence[0].metric == "website.identity":
            findings.append(Finding(self._id("finding", observation.observation_id, "dormant"), observation.source_identifier, "Dormant Website", .5, (evidence[0].evidence_id,), "The official website observation contains no explicit activity resources", observation.observed_at))
        assessments = AssessmentBuilder().build(observation, tuple(evidence), tuple(findings))
        return AnalysisOutput(observation, tuple(evidence), tuple(findings), assessments)

    def _append(self, observation: Observation, key: str, label: str, matches: tuple[str, ...], finding_type: str, evidence: list[Evidence], findings: list[Finding]) -> None:
        evidence_id = self._id("evidence", observation.observation_id, key)
        confidence = min(1.0, .6 + .1 * (len(matches) - 1))
        evidence.append(Evidence(evidence_id, observation.source_identifier, observation.observation_id, f"website.{key}", {"matches": matches, "description": label}, confidence, "website", {"terms": matches}, observation.observed_at))
        findings.append(Finding(self._id("finding", observation.observation_id, key), observation.source_identifier, finding_type, confidence, (evidence_id,), f"{label} confirmed by: {', '.join(matches)}", observation.observed_at))

    @staticmethod
    def _id(kind: str, observation_id: str, key: str) -> str:
        digest = hashlib.sha256(f"{kind}:{observation_id}:{key}".encode()).hexdigest()[:16]
        return f"website:{kind}:{digest}"

    @staticmethod
    def enter_runtime(output: AnalysisOutput, integration: WebsiteRuntimeIntegration, context: ExecutionContext) -> ExecutionResult:
        return integration.integrate((output.observation, output.evidence, output.findings, output.assessments, ()), context)
