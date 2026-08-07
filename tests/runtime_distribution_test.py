from dataclasses import FrozenInstanceError

import pytest

from src.runtime.distribution import (
    DistributionChannel,
    DistributionContext,
    DistributionEngine,
    DistributionMessage,
    DistributionPlan,
    DistributionPriority,
    DistributionProvider,
    DistributionRegistry,
    DistributionRequest,
    DistributionResult,
    DistributionStatus,
    DistributionTarget,
)


def make_request() -> DistributionRequest:
    channel = DistributionChannel("operations", "dashboard")
    target = DistributionTarget("target-1", channel, "risk-feed")
    message = DistributionMessage("message-1", body="Canonical intelligence update")
    return DistributionRequest("request-1", message, target, DistributionPriority.HIGH)


def test_constructs_immutable_distribution_plan() -> None:
    request = make_request()
    plan = DistributionPlan(plan_id="plan-1", requests=(request,), strategy_name="priority")

    assert plan.requests == (request,)
    assert plan.requests[0].target.channel.channel_type == "dashboard"
    with pytest.raises(FrozenInstanceError):
        plan.strategy_name = "broadcast"  # type: ignore[misc]


def test_request_and_result_contracts() -> None:
    request = make_request()
    result = DistributionResult(
        request_id=request.request_id,
        status=DistributionStatus.DELIVERED,
        provider_name="plugin",
        attempt_count=1,
    )

    assert request.priority is DistributionPriority.HIGH
    assert result.status is DistributionStatus.DELIVERED


def test_provider_registry_and_engine_protocols() -> None:
    assert "deliver" in DistributionProvider.__dict__
    assert "register" in DistributionRegistry.__dict__
    assert "get" in DistributionRegistry.__dict__

    class Registry:
        def register(self, name: str, provider: object) -> None:
            self.provider = provider

        def get(self, name: str) -> object | None:
            return getattr(self, "provider", None)

    class Strategy:
        def distribute(self, plan, context, registry):
            return (
                DistributionResult(plan.requests[0].request_id, DistributionStatus.ACCEPTED),
            )

    results = DistributionEngine(Registry()).distribute(
        DistributionPlan(requests=(make_request(),)),
        DistributionContext(correlation_id="correlation-1"),
        Strategy(),
    )
    assert results[0].status is DistributionStatus.ACCEPTED


def test_enum_integrity() -> None:
    assert DistributionPriority.CRITICAL > DistributionPriority.HIGH
    assert DistributionStatus.RETRY_PENDING.value == "retry_pending"
