# Canonical Policy Framework

Policies are immutable, versioned, auditable platform contracts. They describe behavior for collectors, analyzers, resolution, memory, correlation, AI, automation, and distribution without embedding evaluation or authorization logic.

`Policy` declares identity, type, version, scope, status, description, and metadata. `PolicyRule` is a declarative, explainable rule; conditions and outcomes are data only. `PolicyDecision` records a future evaluator's applied rules, outcome, confidence, and timestamp. `PolicyContext` preserves execution provenance. `PolicyOverride` models future user or organization-specific customization without applying it.

Version records support reproducible runtime decisions and safe evolution. Scope and status enable platform-wide and subsystem-specific lifecycle management. The protocol-only `PolicyRegistry` allows future providers. AI-assisted decisions can consume the same versioned, explainable contracts, while runtime components remain decoupled from storage and rule engines.
