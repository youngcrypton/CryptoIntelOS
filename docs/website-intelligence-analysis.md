# Website Intelligence Analysis

## Analysis philosophy

Website analysis transforms canonical discovery observations into explicit, reproducible intelligence. Rules inspect only supplied observation payload fields, document types, URLs, named paths, email addresses, and known domains. No network access, AI, LLM, random input, or probabilistic inference participates.

## Evidence generation

The engine generates canonical Kernel `Evidence` for official website identity, documentation and whitepaper availability, public roadmaps, team transparency, hiring, security resources, social presence, ecosystem participation, and contact information. Each record retains its originating observation, matched terms, source, timestamp, confidence, and deterministic identifier.

## Findings

Evidence produces canonical findings including Verified Official Website, Strong Documentation, Public Roadmap, Transparent Team, Active Hiring, Security Focus, Strong Ecosystem Presence, Strong Communication, and Dormant Website. Every finding references its evidence and includes deterministic confidence and a plain-language explanation.

## Assessments

`AssessmentBuilder` groups supported findings into Identity Confidence, Documentation Quality, Team Transparency, Hiring Activity, Security Maturity, Ecosystem Presence, and Communication Quality. Scores are deterministic confidence values normalized to 0–100 under policy `website-deterministic` version `1.0`.

The frozen canonical Assessment model has no explanation field. Assessment rationale remains traceable through its evidence references to the corresponding `Finding.explanation`; Kernel contracts are not modified.

## Runtime integration

`WebsiteAnalysisEngine.enter_runtime` forwards the canonical observation, evidence, findings, and assessments through `WebsiteRuntimeIntegration` and the Platform SDK `RuntimeFacade`. The signal tuple is empty because signal generation belongs to Sprint 4. Runtime, Platform, Kernel, and SDK components remain unchanged.
