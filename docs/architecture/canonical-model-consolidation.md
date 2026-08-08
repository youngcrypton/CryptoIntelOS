# Canonical Model Consolidation

## Purpose

This document defines the single authoritative owner for every canonical business concept in CryptoIntel OS. Legacy DTOs remain importable where compatibility is required, but they are explicitly named `Legacy*`, marked deprecated at module level, and must be adapted before crossing Platform SDK or Runtime boundaries.

## Canonical ownership map

| Concept | Authoritative owner | Canonical public import |
|---|---|---|
| Identity | `src.core_intelligence.identity.Identity` | `from src.core_intelligence import Identity` |
| Entity | `src.core_intelligence.identity.Entity` | `from src.core_intelligence import Entity` |
| Project | Identity `Entity` with `EntityType.PROJECT` | `from src.core_intelligence import Entity, EntityType` |
| Identifier | `src.core_intelligence.identity.Identifier` | `from src.core_intelligence import Identifier` |
| Observation | `src.core_intelligence.models.Observation` | `from src.core_intelligence import Observation` |
| Evidence | `src.core_intelligence.models.Evidence` | `from src.core_intelligence import Evidence` |
| Finding | `src.core_intelligence.models.Finding` | `from src.core_intelligence import Finding` |
| Assessment | `src.core_intelligence.models.Assessment` | `from src.core_intelligence import Assessment` |
| Signal | `src.core_intelligence.models.Signal` | `from src.core_intelligence import Signal` |
| Relationship | `src.core_intelligence.relationships.Relationship` | `from src.core_intelligence import Relationship` |
| Memory | `src.core_intelligence.memory.MemoryObject` | `from src.core_intelligence import MemoryObject` |
| Policy | `src.core_intelligence.policy.Policy` | `from src.core_intelligence import Policy` |
| Wallet | `src.core_intelligence.onchain.Wallet` | `from src.core_intelligence import Wallet` |
| Token | `src.core_intelligence.onchain.Token` | `from src.core_intelligence import Token` |
| Contract | `src.core_intelligence.onchain.Contract` | `from src.core_intelligence import Contract` |
| On-chain business models | `src.core_intelligence.onchain` | Import the named model from that package |
| Project intelligence profile | `src.unified_intelligence.profile.ProjectIntelligenceProfile` | Import from `src.unified_intelligence.profile` |
| Runtime execution context | `src.runtime.engine.ExecutionContext` | Import from `src.runtime.engine` |

Infrastructure records such as Blockchain Platform chain metadata, source-domain GitHub/Website/Twitter records, persistence rows, adapter results, discovery results, and Runtime graph/compiler objects are not canonical business models. They remain owned by their bounded packages and must not be re-exported as Kernel models.

## Deprecated duplicates

| Compatibility import | Deprecated implementation | Migration |
|---|---|---|
| `src.core_intelligence.models.Entity` | `LegacyEntity` | Use Identity Framework `Entity` and `Identity`. |
| `src.core_intelligence.identity.relationship.Relationship` | `LegacyIdentityRelationship` | Use semantic `core_intelligence.relationships.Relationship`. |
| `src.intelligence.finding.Finding` | `LegacyFinding` | Adapt rule output to canonical `Finding`. |
| `src.intelligence.core.signal.Signal` | `LegacySignal` | Adapt pipeline output to canonical `Signal`. |
| `src.models.intelligence_signal.IntelligenceSignal` | `LegacyIntelligenceSignal` | Use canonical `Signal`. |
| `src.intelligence_core.models.IntelligenceSignal` | `LegacyIntelligenceSignal` | Use canonical `Signal`. |
| `src.intelligence_core.models.IntelligenceProfile` | `LegacyIntelligenceProfile` | Use Unified `ProjectIntelligenceProfile`. |
| `src.models.project.Project` | `LegacyProject` | Use Identity `Entity` with `EntityType.PROJECT`; keep DTO private to persistence. |
| `src.models.project_intelligence_profile.ProjectIntelligenceProfile` | `LegacyProjectIntelligenceProfile` | Use Unified profile. |
| `src.orchestrator.execution_context.ExecutionContext` | `LegacyCollectorExecutionContext` | Use Runtime `ExecutionContext`; adapt collector status separately. |
| `src.core_intelligence.interfaces.context.ExecutionContext` | `LegacyPipelineExecutionContext` | Use Runtime `ExecutionContext`. |

Compatibility aliases preserve existing imports; new code must not import these legacy paths. Deprecation warnings are intentionally not emitted at import time because application startup and existing consumers must remain behaviorally stable.

## Identity construction

`Identity` is now keyword-only. This prevents a canonical name from being silently assigned to `identity_id` when positional arguments are used. Use:

```python
Identity(canonical_name="Example", identifiers=(identifier,))
```

All Unified Intelligence call sites have been migrated to the keyword form.

## Import rules

1. Application and Runtime code imports canonical lifecycle models from `src.core_intelligence` or their authoritative subpackage.
2. Platform SDK collector execution uses `src.runtime.engine.ExecutionContext`.
3. Persistence and legacy rule DTOs remain behind adapters and never enter Runtime directly.
4. Source models remain source-owned and translate to canonical Kernel models at the adapter boundary.
5. A repository-wide ownership test rejects new duplicate class definitions for authoritative model names.

## Future migration

This sprint establishes ownership without deleting compatibility DTOs or changing legacy rule/persistence behavior. Later remediation may add conversion adapters, removal timelines, schema-versioned serialization, and deprecation warnings after all legacy consumers migrate.
