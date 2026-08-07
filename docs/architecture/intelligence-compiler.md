# Intelligence Compiler

The Intelligence Compiler is the first Runtime-layer contract. It consumes canonical kernel objects and emits immutable, storage- and graph-agnostic intermediate representations (IR). It performs no graph writes, correlation, inference, or AI reasoning.

`NodeIR` and `EdgeIR` describe graph-ready nodes and edges while retaining labels, properties, references, provenance, direction, and timestamps. `TimelineIR` preserves temporal validity and ordering. `ProvenanceIR` makes source links explicit. `GraphProjection` composes these values into a complete projection, and `CompilerResult` packages the projection with execution context.

`CompilerContext` and `CompilerPolicy` make execution and future configuration reproducible. `Compiler` and `CompilerRegistry` are protocols for distributed or plugin implementations. Future graph adapters can translate the IR to any graph technology without changing kernel contracts.
