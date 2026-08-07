# Twitter Signal Generation

## Signal philosophy

Twitter signals are actionable conclusions built from the complete canonical intelligence chain. Generators do not act directly on raw text: an observation must first produce evidence, a finding, and a matching assessment. Low-confidence chains are rejected.

## Signal lifecycle

The lifecycle is `Observation → Evidence → Finding → Assessment → Signal`. The signal engine evaluates registered deterministic generators and returns canonical Kernel `Signal` instances alongside the unchanged upstream records.

## Explainability

Every signal names the findings and assessments that activated its rule. It includes a concrete recommendation, severity, confidence, and explanation. No AI, LLM, random input, or probabilistic inference is involved.

## Provenance

`Signal.supporting_evidence` retains the canonical evidence identifiers referenced by its findings and assessments. The signal entity reference and timestamp are inherited from the originating observation, enabling traversal back through every lifecycle stage.

## Confidence

Confidence is the deterministic mean of the supporting finding and assessment confidence values, capped at 1.0 and rounded reproducibly. Signals below 0.6 confidence are not emitted. Compound signals such as Hidden Gem Candidate and Early Project require multiple assessment categories.

## Runtime integration

`TwitterSignalEngine.enter_runtime` forwards the observation, evidence, findings, assessments, and signals through `TwitterRuntimeIntegration` and the Platform SDK `RuntimeFacade`. Runtime, Kernel, Platform, and SDK code remain unchanged.

## Future AI enhancement opportunities

Later releases may add AI-assisted context classification, contradiction detection, and cross-source corroboration before deterministic signal rules execute. Such enhancements should retain canonical provenance, expose model uncertainty, and never replace the reproducible rule path silently.
