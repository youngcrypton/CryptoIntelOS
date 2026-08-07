# Runtime Execution Engine

Runtime II provides the coordinator contracts for executing the Intelligence Operating System pipeline. The engine owns lifecycle boundaries and stage ordering; it never analyzes intelligence, performs graph work, reasons with AI, schedules work, or persists data.

`ExecutionContext` is immutable execution metadata. `ExecutionLifecycle` records the current state and transition history. `RuntimePipeline` preserves an explicit ordered tuple of canonical stages. `ExecutionEngine` offers lightweight initialize, execute, and shutdown boundaries, returning immutable `ExecutionResult` values. `ExecutionEvent` describes lifecycle and stage events. `ExecutionRegistry` and `RuntimeComponent` are protocols for future plugins.

The model is compatible with future asynchronous and distributed implementations because context, pipeline, events, and results are serializable contracts with no process-local storage assumptions. Components can be registered per stage without coupling the engine to intelligence implementations.
