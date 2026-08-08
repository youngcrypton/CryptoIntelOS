from datetime import UTC, datetime

import pytest

from src.core_intelligence.interfaces.context import LegacyPipelineExecutionContext
from src.core_intelligence.models import Observation
from src.platform_sdk import RuntimeFacade, UnsupportedRuntimeTypeError, execute_synchronously
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState
from src.runtime.synchronous import SynchronousRuntime


NOW = datetime(2026, 8, 8, tzinfo=UTC)


def observation() -> Observation:
    return Observation("observation-1", "test", "source-1", "1", NOW, NOW, "1", "checksum", {"provenance": "preserved", "trace_id": "trace-1"})


def test_facade_preserves_projection_and_execution_metadata() -> None:
    canonical = (observation(), (), (), (), ())
    context = ExecutionContext("execution-1", "1.0", NOW, (("trace_id", "trace-1"),))
    received = []

    def entrypoint(output, supplied_context):
        received.append((output, supplied_context))
        return ExecutionResult(supplied_context.execution_id, ExecutionState.COMPLETED)

    RuntimeFacade(entrypoint).integrate(canonical, context)
    assert received == [(canonical, context)]
    assert received[0][0][0].raw_payload["provenance"] == "preserved"
    assert received[0][1].metadata == (("trace_id", "trace-1"),)


@pytest.mark.parametrize("unsupported", [object(), (object(), (), (), (), ())])
def test_facade_rejects_non_canonical_objects(unsupported: object) -> None:
    context = ExecutionContext("execution-1", "1.0", NOW)
    with pytest.raises(UnsupportedRuntimeTypeError):
        RuntimeFacade(lambda output, supplied: None).integrate(unsupported, context)  # type: ignore[arg-type,return-value]


def test_facade_rejects_legacy_execution_context() -> None:
    legacy = LegacyPipelineExecutionContext("execution-1", "source", NOW)
    with pytest.raises(UnsupportedRuntimeTypeError):
        RuntimeFacade(lambda output, supplied: None).integrate(  # type: ignore[arg-type,return-value]
            (observation(), (), (), (), ()), legacy  # type: ignore[arg-type]
        )


def test_platform_sdk_is_the_synchronous_runtime_entry() -> None:
    result = execute_synchronously(SynchronousRuntime(), (observation(), (), (), (), ()), ExecutionContext("execution-1", "1.0", NOW))
    assert result.execution.final_state is ExecutionState.COMPLETED


def test_runtime_rejects_non_canonical_objects_defensively() -> None:
    with pytest.raises(TypeError, match="canonical objects only"):
        SynchronousRuntime().execute("execution-1", (object(),))  # type: ignore[arg-type]
