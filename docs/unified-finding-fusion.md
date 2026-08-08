# Unified Finding Fusion

## Philosophy

Unified Finding Fusion creates explainable project-level findings from canonical application findings already linked to a unified project identity. It preserves originating findings and evidence rather than replacing them or inferring missing conclusions.

## Project-level findings

`ProjectFinding` retains the `IdentityBundle`, exact finding category, original `FindingReference` objects, supporting evidence identifiers, source provenance, traceability records, and deterministic confidence. `ProjectFindingGroup` collects those findings for one canonical project identifier.

## Deterministic grouping

Findings are grouped only when the IdentityBundle identifier, finding category, and exact sorted supporting-evidence set are identical. Findings with different evidence or categories remain independent. Confidence is the explicit mean of originating canonical finding confidence values.

## Provenance and traceability

Source ownership is resolved through `UnifiedEvidenceBundle` references. Every project finding retains original finding identifiers and supporting evidence. Each trace records the source, evidence set, and deterministic group key.

## Relationship to Unified Evidence

Unified Evidence supplies the provenance map used to attribute canonical findings to GitHub, Twitter, Website, Wallet, or other future sources. Finding Fusion does not alter evidence, perform entity linking, or generate assessments.

## Future AI reasoning

Future reasoning may consume project findings, but it must remain a separate layer. Any AI extension must preserve these deterministic groups, source provenance, confidence, and complete traceability.
