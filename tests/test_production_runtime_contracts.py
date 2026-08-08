from datetime import UTC, datetime

import pytest

from src.runtime.durable import (
    CheckpointStore, ExecutionCheckpoint, ExecutionJob, ExecutionManager,
    ExecutionRecovery, ExecutionReplay, ExecutionSnapshot, ExecutionState,
    InvalidTransitionError, LifecycleManager,
)
from src.runtime.events import EventBus, EventMetadata, EventRegistry, RuntimeEvent, RuntimeEventType
from src.runtime.observability import HealthCheck, HealthRegistry, HealthStatus, Trace
from src.runtime.providers import CapabilityRegistry, ProviderCapability, ProviderDescriptor, ProviderHealth, ProviderMonitor, ProviderStatus


NOW = datetime(2026, 8, 8, tzinfo=UTC)


class MemoryStore:
    def __init__(self): self.jobs = {}; self.snapshots = {}; self.checkpoints = {}
    def save(self, job): self.jobs[job.execution_id] = job
    def get(self, execution_id): return self.jobs.get(execution_id)
    def update(self, snapshot): self.snapshots[snapshot.execution_id] = snapshot
    def save_checkpoint(self, checkpoint): self.checkpoints[checkpoint.execution_id] = checkpoint
    def latest(self, execution_id): return self.checkpoints.get(execution_id)


def test_durable_creation_checkpoint_recovery_and_replay():
    store = MemoryStore()
    manager = ExecutionManager(store, store)
    snapshot = manager.create(ExecutionJob("exec-1", {"kind": "canonical"}))
    queued = LifecycleManager().transition(snapshot, ExecutionState.QUEUED).snapshot
    checkpoint = ExecutionCheckpoint("exec-1", "compile", 1, ExecutionState.RUNNING, created_at=NOW)
    manager.checkpoint(checkpoint)
    recovered = ExecutionRecovery().recover(queued, checkpoint)
    replayed = ExecutionReplay().replay(recovered, checkpoint)
    assert replayed.state is ExecutionState.QUEUED
    assert replayed.checkpoint is checkpoint


def test_lifecycle_rejects_invalid_transition():
    with pytest.raises(InvalidTransitionError):
        LifecycleManager().transition(ExecutionSnapshot("exec-1", ExecutionState.COMPLETED, None), ExecutionState.RUNNING)


def test_event_bus_dispatches_deterministically():
    received = []
    class Subscriber:
        def handle(self, event): received.append(event)
    registry = EventRegistry(); registry.subscribe(RuntimeEventType.EXECUTION_CREATED, Subscriber())
    event = RuntimeEvent(RuntimeEventType.EXECUTION_CREATED, EventMetadata("e", "c", "t"))
    EventBus(__import__("src.runtime.events", fromlist=["EventDispatcher"]).EventDispatcher(registry)).publish(event)
    assert received == [event]


def test_observability_and_provider_contracts():
    health = HealthRegistry(); check = HealthCheck("provider", HealthStatus.HEALTHY); health.register(check)
    descriptor = ProviderDescriptor("provider-1", "Fixture", capabilities=(ProviderCapability("collect"),))
    monitor = ProviderMonitor(); monitor.record(descriptor.provider_id, ProviderHealth(ProviderStatus.HEALTHY))
    assert health.get("provider") is check
    assert CapabilityRegistry().supports(descriptor, descriptor.capabilities)
    assert monitor.health("provider-1").status is ProviderStatus.HEALTHY
    assert Trace("t", "c", "e").execution_id == "e"
