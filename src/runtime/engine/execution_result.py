from dataclasses import dataclass
from .execution_state import ExecutionState
@dataclass(frozen=True, slots=True)
class ExecutionResult:
    execution_id: str
    final_state: ExecutionState
    completed_stages: tuple[str, ...] = ()
    failed_stage: str | None = None
    metadata: tuple[tuple[str,str], ...] = ()
