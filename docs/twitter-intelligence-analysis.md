# Twitter Intelligence Analysis

## Analysis philosophy

Twitter analysis converts canonical observations into reproducible intelligence without AI or external calls. Rules inspect explicit text, record matched terms, and preserve the originating observation as provenance. The same observation always produces the same evidence, findings, assessments, identifiers, scores, and confidence values.

## Evidence generation

The analysis engine emits canonical `Evidence` for founder and organization identity, developer and hiring activity, funding and partnership mentions, product releases, ecosystem and narrative participation, and community engagement. Evidence values contain the explicit rule matches; provenance records the terms used by the deterministic rule.

When an observation contains no developer or product activity terms, the engine records absence-of-activity evidence that supports a `Dormant Activity` finding.

## Finding generation

Each matched evidence record produces a canonical `Finding` with its supporting evidence identifier, deterministic confidence, and a plain-language explanation. Supported findings include active founders and development teams, hiring, funding, partnerships, product shipping, ecosystem expansion, strong community activity, emerging narratives, organization activity, and dormant activity.

## Assessment generation

The assessment builder groups relevant findings into founder credibility, team visibility, community health, ecosystem presence, narrative strength, partnership confidence, funding confidence, and product maturity. Scores are normalized to 0–100 and confidence to 0–1 under policy `twitter-deterministic` version `1.0`.

The frozen canonical `Assessment` model does not contain an explanation field. Assessment rationale therefore remains traceable through `Assessment.evidence` to the corresponding canonical `Finding.explanation`; the Kernel model is not modified.

## Runtime integration

`TwitterAnalysisEngine.enter_runtime` forwards the canonical observation, evidence, findings, and assessments through `TwitterRuntimeIntegration` and the Platform SDK `RuntimeFacade`. The signal tuple is deliberately empty because signal generation belongs to Sprint 4. The Runtime is unchanged.

## Current limitations

- Analysis is keyword-based and does not infer context, negation, sarcasm, or identity beyond explicit text.
- Confidence reflects deterministic term matches, not independent source verification.
- Assessments are created only when supporting findings exist.
- No signals, LLM calls, network requests, or cross-observation correlation are performed.
