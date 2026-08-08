# Unified Assessment Fusion

## Philosophy

Unified Assessment Fusion creates deterministic project-level judgments from canonical assessments already anchored to unified identity, evidence, and findings. It preserves source judgments rather than inventing missing assessments or applying AI reasoning.

## Project-level assessments

`ProjectAssessment` retains identity, category, mean score, originating assessment references, supporting project findings, supporting evidence, provenance, traceability, and confidence. `ProjectAssessmentGroup` contains all judgments for one canonical project identifier.

Supported categories include Engineering Maturity, Community Health, Treasury Strength, Product Maturity, Execution Velocity, Security Readiness, Governance Quality, Adoption Momentum, Operational Risk, and Market Confidence.

## Deterministic grouping

Assessments are grouped only when identity, assessment category, exact supporting-finding identifiers, and exact supporting-evidence identifiers match. Supporting project findings are resolved through explicit evidence intersection. Unrelated assessments remain separate.

## Provenance and traceability

Source ownership comes from `UnifiedEvidenceBundle`. Each trace retains the original assessment identifier, source, finding references, evidence references, and deterministic group key. Confidence and score are explicit means of the originating canonical assessments.

## Relationship to Project Findings

Project Findings provide the explainable interpretations supporting project-level judgments. Assessment Fusion consumes them but does not alter or regenerate findings or evidence.

## Future AI reasoning

Future reasoning may consume `ProjectAssessmentGroup`, but it must remain a separate layer and preserve deterministic assessment provenance, confidence, evidence, and finding traceability.
