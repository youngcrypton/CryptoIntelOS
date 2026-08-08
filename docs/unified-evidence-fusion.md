# Unified Evidence Fusion

## Philosophy

Unified Evidence Fusion creates one deterministic evidence view for an existing `IdentityBundle`. It preserves source ownership and original canonical evidence rather than rewriting, inferring, or weakening provenance.

## Deterministic grouping

Evidence is grouped only by the IdentityBundle project identifier, source, evidence type (`metric`), and exact timestamp. Evidence from unrelated identities or different source/type/time keys remains separate. No AI, probabilistic matching, or missing-evidence inference participates.

## Provenance and traceability

Each `EvidenceReference` retains the original canonical `Evidence`. `EvidenceTrace` records its evidence identifier, source, observation origin, and deterministic group key. The bundle also carries source maps, provenance pairs, and a complete traceability list.

## Relationship to IdentityBundle

The IdentityBundle is the identity anchor produced by Unified Entity Linking. Unified Evidence Fusion accepts that anchor as input and attaches evidence only to its canonical project identifier. It does not perform entity linking or finding generation.

## Future confidence weighting

Future pluggable strategies may apply explicit source policies or confidence weighting. Such strategies must preserve every originating evidence reference, retain explainable rationale, and remain behind `EvidenceFusionStrategy` without changing the canonical Evidence Framework.
