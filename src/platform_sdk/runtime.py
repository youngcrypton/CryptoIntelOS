from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeAlias

from src.core_intelligence.models import Assessment, Evidence, Finding, Observation, Signal
from src.runtime.engine import ExecutionContext, ExecutionResult
from src.runtime.synchronous import SynchronousRuntime, SynchronousRuntimeResult

from .pipeline import IntegrationPipeline

CanonicalOutput: TypeAlias = tuple[
    Observation,
    tuple[Evidence, ...],
    tuple[Finding, ...],
    tuple[Assessment, ...],
    tuple[Signal, ...],
]
CanonicalRuntimeObject: TypeAlias = Observation | Evidence | Finding | Assessment | Signal


class UnsupportedRuntimeTypeError(TypeError):
    """Raised when a non-canonical object attempts to cross the Runtime boundary."""


def validate_canonical_output(output: object) -> CanonicalOutput:
    """Validate the canonical Runtime projection without changing its meaning."""

    if not isinstance(output, tuple) or len(output) != 5:
        raise UnsupportedRuntimeTypeError(
            "Runtime input must be a five-part canonical output tuple"
        )
    observation, evidence, findings, assessments, signals = output
    if not isinstance(observation, Observation):
        raise UnsupportedRuntimeTypeError(
            f"Runtime observation must be Observation, got {type(observation).__name__}"
        )
    _validate_group("evidence", evidence, Evidence)
    _validate_group("findings", findings, Finding)
    _validate_group("assessments", assessments, Assessment)
    _validate_group("signals", signals, Signal)
    return output


def validate_execution_context(context: object) -> ExecutionContext:
    """Require the canonical Runtime execution context."""

    if not isinstance(context, ExecutionContext):
        raise UnsupportedRuntimeTypeError(
            "Runtime context must be src.runtime.engine.ExecutionContext, "
            f"got {type(context).__name__}"
        )
    return context


def flatten_canonical_output(output: CanonicalOutput) -> tuple[CanonicalRuntimeObject, ...]:
    """Flatten a validated projection for the internal synchronous Runtime."""

    observation, evidence, findings, assessments, signals = validate_canonical_output(output)
    return (observation, *evidence, *findings, *assessments, *signals)


def execute_synchronously(
    runtime: SynchronousRuntime,
    output: CanonicalOutput,
    context: ExecutionContext,
) -> SynchronousRuntimeResult:
    """Supported SDK gateway into the synchronous Runtime."""

    canonical_context = validate_execution_context(context)
    return runtime.execute(
        canonical_context.execution_id,
        flatten_canonical_output(output),
    )


def _validate_group(name: str, values: object, expected_type: type[object]) -> None:
    if not isinstance(values, tuple):
        raise UnsupportedRuntimeTypeError(f"Runtime {name} must be a tuple")
    for value in values:
        if not isinstance(value, expected_type):
            raise UnsupportedRuntimeTypeError(
                f"Runtime {name} must contain only {expected_type.__name__}, "
                f"got {type(value).__name__}"
            )


@dataclass(frozen=True, slots=True)
class RuntimeFacade:
    """Small SDK boundary that delegates execution to an existing Runtime entry point."""

    runtime_entrypoint: Callable[[CanonicalOutput, ExecutionContext], ExecutionResult]
    pipeline: IntegrationPipeline = IntegrationPipeline()

    def integrate(
        self, output: CanonicalOutput, context: ExecutionContext
    ) -> ExecutionResult:
        return self.runtime_entrypoint(
            validate_canonical_output(output),
            validate_execution_context(context),
        )
