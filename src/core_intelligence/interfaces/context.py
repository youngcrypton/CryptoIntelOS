"""Deprecated pipeline-stage context.

Use ``src.runtime.engine.ExecutionContext`` for canonical execution lifecycle data.
"""

__deprecated__ = True

from dataclasses import dataclass, field
from datetime import datetime
from typing import Mapping

from ..models import JsonValue
from .pipeline import PipelineStage


@dataclass(frozen=True, slots=True)
class LegacyPipelineExecutionContext:
    """Immutable context propagated through one intelligence execution."""

    execution_id: str
    pipeline_stage: PipelineStage
    source: str
    started_at: datetime
    metadata: Mapping[str, JsonValue] = field(default_factory=dict)


ExecutionContext = LegacyPipelineExecutionContext
