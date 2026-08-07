# Website Signal Generation

## Purpose

Sprint 4 converts deterministic Website analysis findings and assessments into canonical, explainable signals. It reuses the Website Foundation, Discovery Engine, and Analysis layer without modifying Platform, Kernel, Runtime, or Platform SDK contracts.

## Signal generation

`WebsiteSignalEngine` evaluates an ordered `SignalRegistry`. Each generator requires explicit finding and assessment types, carries forward their evidence references, calculates deterministic confidence, and produces the canonical Kernel `Signal` model.

The default registry generates signals for official website identity, documentation, roadmap visibility, team transparency, hiring, security readiness, ecosystem presence, communication strength, and dormant website risk.

## Runtime integration

`WebsiteSignalEngine.enter_runtime` delegates the observation, evidence, findings, assessments, and generated signals through `WebsiteRuntimeIntegration` and the Platform SDK `RuntimeFacade`. No Website-specific model crosses the canonical runtime boundary.

## Scope

Signal generation performs no collection, crawling, HTTP requests, AI inference, correlation, persistence, scheduling, or vertical-slice orchestration. End-to-end Website orchestration belongs to Sprint 5 and is not part of this sprint.
