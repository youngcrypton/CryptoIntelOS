# Unified Entity Linking

## Philosophy

Unified Entity Linking joins canonical GitHub, Twitter, Website, and Wallet entities into one deterministic project identity. It is evidence-based identity resolution, not AI reasoning, probabilistic matching, or external API enrichment.

## Deterministic matching rules

The linker accepts exact official website URLs and domains, GitHub repository identifiers, Twitter/X identifiers, wallet references, ENS names, canonical names, explicit metadata, and existing Identity Framework identifiers. A link is accepted only when an exact identifier or exact canonical name matches; weak similarity is ignored.

## Explainability and traceability

Every `EntityMatch` retains both candidates, matched identifiers, confidence rationale, and explanation. `IdentityBundle` retains canonical project identity, source-specific references, supporting evidence, confidence, and source entity traceability. The resolved project is represented by the existing `Entity`, `Identity`, and `Identifier` contracts.

## Canonical Identity Framework

The linker reuses `src.core_intelligence.identity` rather than defining parallel entity or identifier models. It creates a deterministic project entity with a stable UUID derived from the canonical project identifier.

## Runtime integration

`UnifiedRuntimeIntegration` forwards the immutable IdentityBundle through the existing Platform SDK `RuntimeFacade`. Runtime and Platform SDK implementations remain unchanged.

## Future probabilistic extensions

Future strategies may evaluate broader evidence under explicit policy, but they must remain pluggable behind `EntityLinkingStrategy`, preserve provenance, expose confidence rationale, and never alter the canonical identity contracts.
