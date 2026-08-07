"""Execution tracing contracts for the canonical pipeline."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping

from ..models import JsonValue
from .pipeline import PipelineStage


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    """Immutable context propagated through one intelligence execution."""

    execution_id: str
    pipeline_stage: PipelineStage
    source: str
    started_at: datetime
    metadata: Mapping[str, JsonValue] = field(default_factory=dict)
