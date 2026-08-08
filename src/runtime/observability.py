"""Stable observability contracts for Runtime executions."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import NewType, Protocol, Any
from enum import StrEnum

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

@dataclass(frozen=True, slots=True)
class Trace:
    trace_id: TraceId; correlation_id: CorrelationId; execution_id: ExecutionId; metadata: tuple[tuple[str, str], ...] = ()
@dataclass(frozen=True, slots=True)
class Span:
    span_id: str; trace_id: TraceId; name: str; started_at: datetime; ended_at: datetime | None = None; metadata: tuple[tuple[str, str], ...] = ()
@dataclass(frozen=True, slots=True)
class ExecutionTimeline:
    execution_id: ExecutionId; spans: tuple[Span, ...] = ()
@dataclass(frozen=True, slots=True)
class RuntimeMetrics:
    execution_id: ExecutionId; counters: tuple[tuple[str, float], ...] = (); timings: tuple[StageTiming, ...] = ()
@dataclass(frozen=True, slots=True)
class StructuredLog:
    level: str; message: str; metadata: tuple[tuple[str, Any], ...] = (); created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
class HealthStatus(StrEnum): UNKNOWN="unknown"; HEALTHY="healthy"; DEGRADED="degraded"; UNHEALTHY="unhealthy"
@dataclass(frozen=True, slots=True)
class HealthCheck:
    name: str
    status: HealthStatus
    detail: str = ""
    checked_at: datetime = field(default_factory=lambda: datetime.now(UTC))
class MetricsCollector(Protocol):
    def record(self, metrics: RuntimeMetrics) -> None: ...
class Tracer(Protocol):
    def start(self, trace: Trace, name: str) -> Span: ...
class Logger(Protocol):
    def emit(self, record: StructuredLog) -> None: ...
class HealthRegistry:
    def __init__(self): self._checks: dict[str, HealthCheck] = {}
    def register(self, check: HealthCheck) -> None: self._checks[check.name] = check
    def get(self, name: str) -> HealthCheck | None: return self._checks.get(name)
    def all(self) -> tuple[HealthCheck, ...]: return tuple(self._checks.values())
