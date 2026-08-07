# Core Intelligence Interfaces

## Purpose

The core intelligence interfaces define how source-agnostic components participate in the CryptoIntel OS execution lifecycle. They depend on the canonical models from Epic A and contain no implementation, source integration, scoring policy, or signal rules.

## Execution lifecycle

```text
Collector -> Observation -> Analyzer -> Evidence -> Resolver -> Finding
          -> Scorer -> Assessment -> Signal Generator -> Signal
```

`PipelineStage` encodes this mandatory order as an integer enum. `ExecutionContext` accompanies component calls with an execution identifier, current stage, source, start time, and extensible tracing metadata. The context is immutable so execution identity cannot be reassigned while work is in progress.

## Interfaces

- **Collector** validates an external source and collects immutable observations. It cannot emit evidence, assessments, or signals through its contract.
- **Analyzer** consumes observations and emits normalized evidence. Supported sources and entity types are declared independently of execution.
- **Resolver** resolves observations and evidence to canonical entities, merges evidence, and produces findings. It declares behavior only; entity-resolution algorithms are outside this sprint.
- **Scorer** consumes findings and emits assessments under an identifiable, versioned scoring policy.
- **SignalGenerator** consumes assessments and emits actionable signals. It declares supported signal types and does not perform scoring.
- **Correlator** combines normalized evidence across supported sources and emits normalized evidence. No correlation algorithm is defined here.
- **ComponentRegistry** is a runtime-checkable protocol for registering each component category and retrieving a named component. Structural typing lets plugin registries conform without inheriting a framework base class.

All executable roles are abstract base classes. Their signatures use canonical models, read-only sequence and mapping interfaces, and explicit execution context. Implementations can therefore be substituted behind stable contracts and tested independently.

## Dependency direction

Source integrations and plugins depend inward on these interfaces. The interfaces depend only on Python's standard library and the canonical domain models. The canonical package never depends on collectors, analyzers, storage, frameworks, or external services. Orchestrators depend on abstractions rather than concrete plugins.

```text
Concrete plugins -> core intelligence interfaces -> canonical models
Orchestrators ----^
```

## Plugin architecture

A plugin implements one or more abstract interfaces, publishes stable component metadata, and registers instances under unique names through `ComponentRegistry`. Registry implementations may later discover entry points, manifests, remote workers, or AI-provided components without changing the component contracts.

Metadata should include stable names and versions where relevant. Scorers must expose policy identity and version through `scoring_policy()`. Components should accept and return canonical records rather than source-specific transport objects.

## Extension guidelines

- Preserve the declared input and output stage for every component.
- Keep external I/O inside collectors; analyzers operate on observations already collected.
- Add capabilities through new implementations and metadata before changing an interface.
- Prefer additive, optional contract evolution and version breaking semantic changes.
- Do not place raw source payloads outside observations.
- Keep implementations stateless where practical so they can later run asynchronously, remotely, or in distributed workers.
- Propagate `ExecutionContext` unchanged except when an orchestrator creates a context for the next pipeline stage.

The current methods are synchronous contracts. Their value-oriented inputs and outputs avoid transport assumptions, allowing future asynchronous adapters or distributed executors without embedding those concerns in the canonical kernel.
