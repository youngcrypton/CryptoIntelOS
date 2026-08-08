from dataclasses import dataclass

from src.core_intelligence.models import Assessment, Evidence, Finding, Signal
from src.unified_intelligence.entity_linking import EntityCandidate


@dataclass(frozen=True, slots=True)
class SourceIntelligence:
    source: str
    candidate: EntityCandidate
    evidence: tuple[Evidence, ...] = ()
    findings: tuple[Finding, ...] = ()
    assessments: tuple[Assessment, ...] = ()
    signals: tuple[Signal, ...] = ()


@dataclass(frozen=True, slots=True)
class ProfileMetadata:
    profile_version: str
    sources: tuple[str, ...]
    runtime_version: str = "1.0"
