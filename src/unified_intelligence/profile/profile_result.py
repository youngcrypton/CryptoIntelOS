from dataclasses import dataclass

from src.runtime.synchronous import SynchronousRuntimeResult

from .project_intelligence_profile import ProjectIntelligenceProfile


@dataclass(frozen=True, slots=True)
class ProfileResult:
    profile: ProjectIntelligenceProfile


@dataclass(frozen=True, slots=True)
class UnifiedIntelligenceExecutionResult:
    profile: ProjectIntelligenceProfile
    runtime: SynchronousRuntimeResult
    console_summary: str
