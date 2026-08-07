# Canonical Intelligence Space

Intelligence Space is the transient working memory used while intelligence is collected, analyzed, resolved, correlated, and scored. Unlike canonical Memory, it is intentionally mutable during execution and does not represent durable history.

`Space` groups an immutable `SpaceContext` with mutable active objects and runtime metadata. `Workspace` scopes one or more spaces for future multi-project execution. Active entity, relationship, evidence, assessment, and signal wrappers expose runtime status without mutating their canonical payloads. `SpaceEvent` describes runtime changes, while `SpaceSnapshot` freezes a point-in-time view without persisting it.

The contracts impose no scheduler, cache, execution engine, graph, or storage backend. Independent spaces and immutable contexts can be coordinated by future concurrent collectors, asynchronous pipelines, streaming systems, or distributed workers. Stable snapshots and typed events can also provide future AI components with explainable runtime state while keeping AI behavior outside this framework. `SpaceRegistry` is a protocol for future runtime providers only.
