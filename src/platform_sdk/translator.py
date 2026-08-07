from typing import Protocol

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation, Signal


class ObservationTranslator(Protocol):
    def to_evidence(self, observation: Observation) -> tuple[Evidence, ...]: ...


class EvidenceTranslator(Protocol):
    def to_findings(self, evidence: tuple[Evidence, ...]) -> tuple[Finding, ...]: ...


class FindingTranslator(Protocol):
    def to_assessments(self, findings: tuple[Finding, ...]) -> tuple[Assessment, ...]: ...


class AssessmentTranslator(Protocol):
    def to_signals(self, assessments: tuple[Assessment, ...]) -> tuple[Signal, ...]: ...
