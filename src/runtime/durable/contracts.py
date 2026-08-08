from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Protocol


class ExecutionState(StrEnum):
    CREATED = "created"; QUEUED = "queued"; RUNNING = "running"; PAUSED = "paused"; RETRYING = "retrying"; COMPLETED = "completed"; FAILED = "failed"; CANCELLED = "cancelled"; TIMED_OUT = "timed_out"


class DurableExecutionError(Exception): pass
class InvalidTransitionError(DurableExecutionError): pass
class ExecutionNotFoundError(DurableExecutionError): pass
class ReplayError(DurableExecutionError): pass


@dataclass(frozen=True, slots=True)
class ExecutionCheckpoint:
    execution_id: str
    stage: str
    sequence: int
    state: ExecutionState
    metadata: tuple[tuple[str, str], ...] = ()
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class ExecutionSnapshot:
    execution_id: str
    state: ExecutionState
    stage: str | None
    checkpoint: ExecutionCheckpoint | None = None
    metadata: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class ExecutionJob:
    execution_id: str
    payload: Any
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class JobContext:
    execution_id: str
    correlation_id: str
    attempt: int = 1
    timeout_seconds: float | None = None
    metadata: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True, slots=True)
class JobResult:
    execution_id: str
    state: ExecutionState
    value: Any = None
    error: str | None = None
    attempts: int = 1


class ExecutionStore(Protocol):
    def save(self, job: ExecutionJob) -> None: ...
    def get(self, execution_id: str) -> ExecutionJob | None: ...
    def update(self, snapshot: ExecutionSnapshot) -> None: ...


class CheckpointStore(Protocol):
    def save(self, checkpoint: ExecutionCheckpoint) -> None: ...
    def latest(self, execution_id: str) -> ExecutionCheckpoint | None: ...


@dataclass(frozen=True, slots=True)
class ExecutionTransition:
    execution_id: str
    source: ExecutionState
    target: ExecutionState
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    reason: str = ""


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 3
    retryable_states: frozenset[ExecutionState] = frozenset({ExecutionState.FAILED, ExecutionState.TIMED_OUT})


class RetryStrategy(Protocol):
    def delay_seconds(self, attempt: int) -> float: ...


@dataclass(frozen=True, slots=True)
class ExponentialRetryStrategy:
    base_seconds: float = 1.0
    def delay_seconds(self, attempt: int) -> float: return self.base_seconds * (2 ** max(0, attempt - 1))


@dataclass(frozen=True, slots=True)
class LifecyclePolicy:
    retry: RetryPolicy = field(default_factory=RetryPolicy)
    timeout_seconds: float | None = None


@dataclass(frozen=True, slots=True)
class LifecycleResult:
    snapshot: ExecutionSnapshot
    transitions: tuple[ExecutionTransition, ...] = ()


_ALLOWED = {
    ExecutionState.CREATED: frozenset({ExecutionState.QUEUED, ExecutionState.CANCELLED}),
    ExecutionState.QUEUED: frozenset({ExecutionState.RUNNING, ExecutionState.CANCELLED}),
    ExecutionState.RUNNING: frozenset({ExecutionState.PAUSED, ExecutionState.COMPLETED, ExecutionState.FAILED, ExecutionState.CANCELLED, ExecutionState.TIMED_OUT}),
    ExecutionState.PAUSED: frozenset({ExecutionState.RUNNING, ExecutionState.CANCELLED}),
    ExecutionState.RETRYING: frozenset({ExecutionState.QUEUED, ExecutionState.FAILED}),
    ExecutionState.COMPLETED: frozenset(), ExecutionState.FAILED: frozenset({ExecutionState.RETRYING}), ExecutionState.CANCELLED: frozenset(), ExecutionState.TIMED_OUT: frozenset({ExecutionState.RETRYING}),
}


class LifecycleManager:
    def transition(self, snapshot: ExecutionSnapshot, target: ExecutionState, reason: str = "") -> LifecycleResult:
        if target not in _ALLOWED[snapshot.state]: raise InvalidTransitionError(f"{snapshot.state} -> {target} is not allowed")
        updated = ExecutionSnapshot(snapshot.execution_id, target, snapshot.stage, snapshot.checkpoint, snapshot.metadata)
        return LifecycleResult(updated, (ExecutionTransition(snapshot.execution_id, snapshot.state, target, reason=reason),))


class ExecutionManager:
    def __init__(self, store: ExecutionStore, checkpoints: CheckpointStore | None = None, lifecycle: LifecycleManager | None = None) -> None:
        self.store = store; self.checkpoints = checkpoints; self.lifecycle = lifecycle or LifecycleManager()
    def create(self, job: ExecutionJob) -> ExecutionSnapshot:
        snapshot = ExecutionSnapshot(job.execution_id, ExecutionState.CREATED, None, metadata=job.metadata); self.store.save(job); self.store.update(snapshot); return snapshot
    def checkpoint(self, checkpoint: ExecutionCheckpoint) -> None:
        if self.checkpoints is None: raise DurableExecutionError("checkpoint store is not configured")
        self.checkpoints.save(checkpoint)
    def transition(self, snapshot: ExecutionSnapshot, target: ExecutionState, reason: str = "") -> LifecycleResult:
        result = self.lifecycle.transition(snapshot, target, reason); self.store.update(result.snapshot); return result
    def cancel(self, snapshot: ExecutionSnapshot, reason: str = "cancelled") -> LifecycleResult: return self.transition(snapshot, ExecutionState.CANCELLED, reason)
    def retry(self, snapshot: ExecutionSnapshot, policy: RetryPolicy, attempt: int) -> LifecycleResult:
        if snapshot.state not in policy.retryable_states or attempt >= policy.max_attempts: raise InvalidTransitionError("execution is not retryable")
        return self.transition(snapshot, ExecutionState.RETRYING, f"retry attempt {attempt + 1}")


class ExecutionReplay:
    def replay(self, snapshot: ExecutionSnapshot, checkpoint: ExecutionCheckpoint | None = None) -> ExecutionSnapshot:
        return ExecutionSnapshot(snapshot.execution_id, ExecutionState.QUEUED, checkpoint.stage if checkpoint else snapshot.stage, checkpoint, snapshot.metadata)


class ExecutionRecovery:
    def recover(self, snapshot: ExecutionSnapshot, checkpoint: ExecutionCheckpoint | None) -> ExecutionSnapshot:
        if checkpoint is None: raise ReplayError(f"no checkpoint for {snapshot.execution_id}")
        return ExecutionSnapshot(snapshot.execution_id, ExecutionState.PAUSED, checkpoint.stage, checkpoint, snapshot.metadata)
