from dataclasses import FrozenInstanceError

from src.core_intelligence.models import Observation
from src.platform_sdk import (
    CANONICAL_LIFECYCLE,
    IntegrationMetadata,
    IntegrationPipeline,
    LifecycleStage,
    RuntimeFacade,
    SourceAdapter,
    SourceCollector,
    ValidationResult,
)
from src.runtime.engine import ExecutionContext, ExecutionResult, ExecutionState


def test_protocol_contracts_are_exposed() -> None:
    assert "collect" in SourceCollector.__dict__
    assert "to_observation" in SourceAdapter.__dict__
    assert "valid" in ValidationResult.__dict__


def test_pipeline_and_lifecycle_are_ordered_and_immutable() -> None:
    pipeline = IntegrationPipeline()
    assert pipeline.stages == CANONICAL_LIFECYCLE
    assert pipeline.stages == (
        LifecycleStage.INITIALIZE,
        LifecycleStage.COLLECT,
        LifecycleStage.TRANSLATE,
        LifecycleStage.EXECUTE,
        LifecycleStage.SHUTDOWN,
    )
    try:
        pipeline.stages = ()  # type: ignore[misc]
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError("pipeline must be immutable")


def test_metadata_and_runtime_facade() -> None:
    metadata = IntegrationMetadata("Collector", "source", "Adapter", "1.0.0", ("history",))
    observed = Observation("observation-1", "source", "source-1", "1", __import__("datetime").datetime.now(__import__("datetime").UTC), __import__("datetime").datetime.now(__import__("datetime").UTC), "1", "checksum", {})
    context = ExecutionContext("execution-1", "1.0", observed.collected_at)
    calls = []

    def entrypoint(output, context):
        calls.append((output, context))
        return ExecutionResult(context.execution_id, ExecutionState.COMPLETED)

    result = RuntimeFacade(entrypoint).integrate((observed, (), (), (), ()), context)
    assert metadata.source == "source"
    assert result.final_state is ExecutionState.COMPLETED
    assert calls[0][1] is context
