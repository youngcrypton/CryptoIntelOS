from dataclasses import dataclass
from .execution_context import ExecutionContext
from .execution_lifecycle import ExecutionLifecycle
from .runtime_pipeline import RuntimePipeline
@dataclass(slots=True)
class Execution:
    context: ExecutionContext
    pipeline: RuntimePipeline
    lifecycle: ExecutionLifecycle = ExecutionLifecycle()
