"""Stable observability contracts for Runtime executions."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import NewType

ExecutionId = NewType("ExecutionId", str)
CorrelationId = NewType("CorrelationId", str)
TraceId = NewType("TraceId", str)


@dataclass(frozen=True, slots=True)
class StageTiming:
    stage: str
    started_at: datetime
    completed_at: datetime
    duration_ms: float


@dataclass(frozen=True, slots=True)
class ExecutionMetrics:
    execution_id: ExecutionId
    correlation_id: CorrelationId | None = None
    trace_id: TraceId | None = None
    stages: tuple[StageTiming, ...] = ()
    counters: tuple[tuple[str, int], ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
