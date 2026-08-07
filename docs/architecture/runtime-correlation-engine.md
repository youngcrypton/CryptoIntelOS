# Runtime Correlation Engine

The Correlation Engine turns canonical runtime and kernel artifacts into explainable correlation objects. It never reads collectors or raw payloads, performs AI reasoning, emits signals, or scores projects.

`EvidenceBundle` and `GraphBundle` provide explicit inputs. `Correlation` records participating entities, evidence, relationships, confidence, explanation, provenance, and time. Candidates, groups, rules, and policies remain immutable data contracts. `CorrelationStrategy` and `CorrelationRegistry` enable deterministic plugins and future AI-assisted strategies without source coupling. Graph bundles can be supplied by the Knowledge Graph foundation while Memory remains authoritative.
