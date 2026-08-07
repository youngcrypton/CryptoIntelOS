from dataclasses import dataclass
from .execution_state import ExecutionState
@dataclass(frozen=True, slots=True)
class ExecutionLifecycle:
    state: ExecutionState = ExecutionState.CREATED
    transitions: tuple[ExecutionState, ...] = (ExecutionState.CREATED,)
