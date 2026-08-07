# Runtime VI: Automation Engine

## Automation philosophy

The Automation Engine converts canonical Runtime and Kernel intelligence into deterministic, explainable action plans. It is source agnostic and policy driven: collectors, notification providers, schedulers, and other delivery infrastructure remain outside this package.

## Decision versus execution

Automation answers what should happen. It does not perform the action. `AutomationEngine` selects a registered strategy, supplies immutable context and policy, and returns an immutable result containing proposed plans. `AutomationExecution` is only the canonical record shape reserved for a future executor.

## Action plans

`AutomationPlan` identifies an ordered tuple of canonical actions and records priority, explanation, supporting reasoning, and an aware timestamp. Actions describe intent and parameters without importing or calling an implementation provider. Supported canonical intents include notify, watch, archive, escalate, schedule, export, webhook, and dashboard pin.

## Trigger model

`AutomationTrigger` describes the runtime event that can activate a rule. `AutomationCondition` carries declarative field, operator, and value data. This layer deliberately defines no condition evaluator, keeping policy representation separate from business logic.

## Policy integration

An `AutomationPolicy` groups immutable rules and a default priority. Rules bind triggers and conditions to proposed actions. Pluggable `AutomationStrategy` implementations interpret these contracts; an `AutomationRegistry` resolves strategies without coupling the engine to concrete plugins.

## Future workflow execution

Future workflow components can consume plans and produce execution records while preserving the decision/execution boundary. Notification, scheduling, retry, approval, and provider-specific concerns belong to those downstream components.

## Distributed execution compatibility

Plans, actions, contexts, and results use explicit, transport-friendly data contracts and stable identifiers. Tuple-based collections and frozen dataclasses prevent local mutation. A future dispatcher can serialize plans, route them to workers, apply idempotency using `plan_id`, and report execution state without changing the Automation Engine.
