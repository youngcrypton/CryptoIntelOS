from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Protocol

class RuntimeEventType(StrEnum):
    EXECUTION_CREATED="execution_created"; EXECUTION_QUEUED="execution_queued"; EXECUTION_STARTED="execution_started"; COMPILER_COMPLETED="compiler_completed"; GRAPH_UPDATED="graph_updated"; CORRELATION_COMPLETED="correlation_completed"; REASONING_COMPLETED="reasoning_completed"; AUTOMATION_COMPLETED="automation_completed"; DISTRIBUTION_COMPLETED="distribution_completed"; EXECUTION_COMPLETED="execution_completed"; EXECUTION_FAILED="execution_failed"
@dataclass(frozen=True, slots=True)
class EventMetadata:
    execution_id: str; correlation_id: str; trace_id: str; sequence: int = 0; created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
@dataclass(frozen=True, slots=True)
class RuntimeEvent:
    event_type: RuntimeEventType; metadata: EventMetadata; payload: Any = None
class ExecutionCreated(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.EXECUTION_CREATED, metadata, payload)
class ExecutionQueued(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.EXECUTION_QUEUED, metadata, payload)
class ExecutionStarted(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.EXECUTION_STARTED, metadata, payload)
class CompilerCompleted(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.COMPILER_COMPLETED, metadata, payload)
class GraphUpdated(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.GRAPH_UPDATED, metadata, payload)
class CorrelationCompleted(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.CORRELATION_COMPLETED, metadata, payload)
class ReasoningCompleted(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.REASONING_COMPLETED, metadata, payload)
class AutomationCompleted(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.AUTOMATION_COMPLETED, metadata, payload)
class DistributionCompleted(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.DISTRIBUTION_COMPLETED, metadata, payload)
class ExecutionCompleted(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.EXECUTION_COMPLETED, metadata, payload)
class ExecutionFailed(RuntimeEvent):
    def __init__(self, metadata: EventMetadata, payload: Any = None): super().__init__(RuntimeEventType.EXECUTION_FAILED, metadata, payload)
@dataclass(frozen=True, slots=True)
class EventEnvelope:
    event: RuntimeEvent; source: str = "runtime"
class EventPublisher(Protocol):
    def publish(self, event: RuntimeEvent) -> None: ...
class EventSubscriber(Protocol):
    def handle(self, event: RuntimeEvent) -> None: ...
class EventRegistry:
    def __init__(self): self._items: dict[RuntimeEventType, list[EventSubscriber]] = {}
    def subscribe(self, event_type: RuntimeEventType, subscriber: EventSubscriber) -> None: self._items.setdefault(event_type, []).append(subscriber)
    def subscribers(self, event_type: RuntimeEventType) -> tuple[EventSubscriber, ...]: return tuple(self._items.get(event_type, ()))
class EventDispatcher:
    def __init__(self, registry: EventRegistry): self.registry = registry
    def dispatch(self, event: RuntimeEvent) -> None:
        for subscriber in self.registry.subscribers(event.event_type): subscriber.handle(event)
class EventBus:
    def __init__(self, dispatcher: EventDispatcher | None = None): self.dispatcher = dispatcher or EventDispatcher(EventRegistry())
    def publish(self, event: RuntimeEvent) -> None: self.dispatcher.dispatch(event)
