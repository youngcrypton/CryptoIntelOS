from dataclasses import FrozenInstanceError
from datetime import UTC, datetime

import pytest

from src.runtime.automation import (
    AutomationAction,
    AutomationActionType,
    AutomationCondition,
    AutomationContext,
    AutomationEngine,
    AutomationPlan,
    AutomationPolicy,
    AutomationPriority,
    AutomationRegistry,
    AutomationRule,
    AutomationStatus,
    AutomationTrigger,
)


def test_constructs_immutable_action_plan() -> None:
    action = AutomationAction(AutomationActionType.WATCH, {"asset": "BTC"}, "Track movement")
    plan = AutomationPlan(
        plan_id="plan-1",
        actions=(action,),
        priority=AutomationPriority.HIGH,
        explanation="Material movement detected",
        supporting_reasoning=("confidence exceeded threshold",),
        timestamp=datetime.now(UTC),
    )

    assert plan.actions == (action,)
    with pytest.raises(FrozenInstanceError):
        plan.priority = AutomationPriority.LOW  # type: ignore[misc]


def test_trigger_condition_and_rule_are_declarative() -> None:
    trigger = AutomationTrigger("risk-change", "intelligence.updated", {"version": 1})
    condition = AutomationCondition("risk_score", "gte", 0.8)
    rule = AutomationRule("escalate-risk", trigger, (condition,), (AutomationAction("escalate"),))

    assert rule.trigger.event_type == "intelligence.updated"
    assert rule.conditions[0].operator == "gte"


def test_registry_protocol_and_engine_contract() -> None:
    assert "register" in AutomationRegistry.__dict__
    assert "get" in AutomationRegistry.__dict__

    class Strategy:
        def decide(self, context: AutomationContext, policy: AutomationPolicy) -> tuple[AutomationPlan, ...]:
            return (AutomationPlan(explanation=policy.name),)

    class Registry:
        def register(self, name: str, strategy: Strategy) -> None:
            self.strategy = strategy

        def get(self, name: str) -> Strategy | None:
            return getattr(self, "strategy", None)

    registry = Registry()
    registry.register("default", Strategy())
    result = AutomationEngine(registry).decide(AutomationContext(), AutomationPolicy("policy"), "default")
    assert result.status is AutomationStatus.PROPOSED
    assert result.plans[0].explanation == "policy"


def test_enum_integrity() -> None:
    assert AutomationPriority.CRITICAL > AutomationPriority.HIGH
    assert AutomationStatus.PROPOSED.value == "proposed"
    assert AutomationActionType.DASHBOARD_PIN.value == "dashboard_pin"
