from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from .pipeline_stage import PipelineStage
class ExecutionEventType(StrEnum):
    EXECUTION_STARTED="execution_started"; STAGE_STARTED="stage_started"; STAGE_COMPLETED="stage_completed"; STAGE_FAILED="stage_failed"; EXECUTION_COMPLETED="execution_completed"; EXECUTION_CANCELLED="execution_cancelled"
@dataclass(frozen=True, slots=True)
class ExecutionEvent:
    execution_id: str
    event_type: ExecutionEventType
    timestamp: datetime
    stage: PipelineStage | None = None
