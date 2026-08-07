from datetime import UTC, datetime
from typing import get_type_hints
import pytest
from src.runtime.engine import *
def test_lifecycle_context_and_ordered_execution():
    pipeline=RuntimePipeline((PipelineStage.COLLECT, PipelineStage.ANALYZE, PipelineStage.COMPILE))
    engine=ExecutionEngine(); context=engine.initialize("exec-1", pipeline); result=engine.execute(context, pipeline)
    assert context.execution_id == result.execution_id
    assert result.completed_stages == ("collect", "analyze", "compile")
    assert result.final_state is ExecutionState.COMPLETED
def test_immutable_contracts_and_events():
    context=ExecutionContext("x", "1.0", datetime.now(UTC))
    with pytest.raises(Exception): context.execution_id="changed"
    event=ExecutionEvent("x", ExecutionEventType.STAGE_STARTED, datetime.now(UTC), PipelineStage.COLLECT)
    assert event.stage is PipelineStage.COLLECT
def test_registry_and_enum_integrity():
    assert "register" in ExecutionRegistry.__dict__
    assert ExecutionState.CANCELLED.value == "cancelled"
    assert get_type_hints(ExecutionResult)["final_state"] is ExecutionState
