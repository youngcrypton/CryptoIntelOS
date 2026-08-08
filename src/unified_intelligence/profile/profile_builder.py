import hashlib
import sys
from datetime import UTC, datetime
from typing import TextIO

from src.core_intelligence.models import Observation, Signal
from src.platform_sdk import execute_synchronously
from src.runtime.engine import ExecutionContext
from src.runtime.synchronous import SynchronousRuntime
from src.unified_intelligence.assessment_fusion import AssessmentFusionContext, AssessmentFusionEngine
from src.unified_intelligence.entity_linking import EntityLinker, LinkingContext
from src.unified_intelligence.evidence_fusion import EvidenceFusionEngine, FusionContext
from src.unified_intelligence.finding_fusion import FindingFusionContext, FindingFusionEngine

from .profile_context import ProfileContext
from .profile_metadata import ProfileMetadata, SourceIntelligence
from .profile_registry import ProfileRegistry
from .profile_result import ProfileResult, UnifiedIntelligenceExecutionResult
from .project_intelligence_profile import ProjectIntelligenceProfile


class DeterministicProfileStrategy:
    strategy_id = "deterministic-profile-v1"

    def build(self, identity, evidence, findings, assessments, signals, metadata, context) -> ProfileResult:
        confidence_values = [identity.confidence.value, evidence.confidence.value]
        confidence_values.extend(item.confidence.value for item in findings.findings)
        confidence_values.extend(item.confidence.value for item in assessments.assessments)
        confidence_values.extend(item.confidence for item in signals)
        confidence = round(sum(confidence_values) / len(confidence_values), 4) if confidence_values else 0.0
        provenance = tuple(evidence.provenance) + tuple(pair for item in findings.findings for pair in item.provenance) + tuple(pair for item in assessments.assessments for pair in item.provenance)
        traceability = tuple(dict.fromkeys((*evidence.traceability, *(trace.finding_id for item in findings.findings for trace in item.traceability), *(trace.assessment_id for item in assessments.assessments for trace in item.traceability), *(signal.signal_id for signal in signals))))
        relationships = tuple((source, reference) for source, reference in identity.traceability)
        profile = ProjectIntelligenceProfile(identity.canonical_project_identifier, identity, evidence, findings, assessments, signals, relationships, provenance, traceability, confidence, metadata, context)
        return ProfileResult(profile)


class ProfileBuilder:
    def __init__(self, registry: ProfileRegistry | None = None) -> None:
        self.registry = registry or self.default_registry()

    @staticmethod
    def default_registry() -> ProfileRegistry:
        registry = ProfileRegistry()
        registry.register(DeterministicProfileStrategy())
        return registry

    def build(self, identity, evidence, findings, assessments, signals: tuple[Signal, ...], metadata: ProfileMetadata, context: ProfileContext) -> ProfileResult:
        return self.registry.get("deterministic-profile-v1").build(identity, evidence, findings, assessments, signals, metadata, context)


class UnifiedIntelligenceVerticalSlice:
    def __init__(self, *, linker=None, evidence=None, findings=None, assessments=None, profiles=None, runtime=None) -> None:
        self.linker = linker or EntityLinker()
        self.evidence = evidence or EvidenceFusionEngine()
        self.findings = findings or FindingFusionEngine()
        self.assessments = assessments or AssessmentFusionEngine()
        self.profiles = profiles or ProfileBuilder()
        self.runtime = runtime or SynchronousRuntime()

    def run(self, sources: tuple[SourceIntelligence, ...], *, output: TextIO | None = None) -> UnifiedIntelligenceExecutionResult:
        if not sources:
            raise ValueError("at least one intelligence source is required")
        now = datetime.now(UTC)
        execution_id = "unified:" + hashlib.sha256("|".join(item.source for item in sources).encode()).hexdigest()[:16]
        identity = self.linker.link(tuple(item.candidate for item in sources), LinkingContext(execution_id)).bundle
        evidence_items = tuple(item for source in sources for item in source.evidence)
        evidence = self.evidence.fuse(identity, evidence_items, FusionContext(execution_id, identity.canonical_project_identifier)).bundle
        finding_items = tuple(item for source in sources for item in source.findings)
        findings = self.findings.fuse(identity, evidence, finding_items, FindingFusionContext(execution_id, identity.canonical_project_identifier)).group
        assessment_items = tuple(item for source in sources for item in source.assessments)
        assessments = self.assessments.fuse(identity, evidence, findings, assessment_items, AssessmentFusionContext(execution_id, identity.canonical_project_identifier)).group
        signals = tuple(item for source in sources for item in source.signals)
        metadata = ProfileMetadata("0.6.0", tuple(item.source for item in sources))
        context = ProfileContext(execution_id, "0.6.0", now.isoformat(), (("source_count", str(len(sources))),))
        profile = self.profiles.build(identity, evidence, findings, assessments, signals, metadata, context).profile
        observation = Observation(f"profile:{identity.canonical_project_identifier}", "unified_intelligence", identity.canonical_project_identifier, "unified-profile", now, now, "0.6.0", hashlib.sha256(repr(profile).encode()).hexdigest(), {"sources": metadata.sources, "confidence": profile.confidence})
        projection = (observation, evidence_items, finding_items, assessment_items, signals)
        runtime = execute_synchronously(
            self.runtime,
            projection,
            ExecutionContext(execution_id, "1.0", now, context.execution_metadata),
        )
        summary = self._summary(profile, runtime)
        print(summary, file=output or sys.stdout)
        return UnifiedIntelligenceExecutionResult(profile, runtime, summary)

    @staticmethod
    def _summary(profile, runtime) -> str:
        return "\n".join((f"Project Identified: {profile.canonical_project_identifier}", f"Sources Linked: {len(profile.runtime_metadata.sources)}", f"Evidence Items: {len(profile.unified_evidence.traceability)}", f"Project Findings: {len(profile.unified_findings.findings)}", f"Project Assessments: {len(profile.unified_assessments.assessments)}", f"Signals: {len(profile.canonical_signals)}", f"Compiler Executed: {len(runtime.compilation.projection.nodes)} nodes", f"Knowledge Graph Updated: {len(runtime.graph.nodes)} nodes", f"Correlation Completed: {runtime.correlation.status.value}", f"Reasoning Completed: {runtime.reasoning.status.value}", f"Automation Planned: {len(runtime.automation.actions)} actions", f"Distribution Planned: {len(runtime.distribution.requests)} requests", f"Execution Successful: {runtime.execution.final_state.value}"))
