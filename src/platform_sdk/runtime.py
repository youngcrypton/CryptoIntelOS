from collections.abc import Callable
from dataclasses import dataclass

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation, Signal
from src.runtime.engine import ExecutionContext, ExecutionResult

from .pipeline import IntegrationPipeline

CanonicalOutput = tuple[Observation, tuple[Evidence, ...], tuple[Finding, ...], tuple[Assessment, ...], tuple[Signal, ...]]


@dataclass(frozen=True, slots=True)
class RuntimeFacade:
    """Small SDK boundary that delegates execution to an existing Runtime entry point."""

    runtime_entrypoint: Callable[[CanonicalOutput, ExecutionContext], ExecutionResult]
    pipeline: IntegrationPipeline = IntegrationPipeline()

    def integrate(
        self, output: CanonicalOutput, context: ExecutionContext
    ) -> ExecutionResult:
        return self.runtime_entrypoint(output, context)
