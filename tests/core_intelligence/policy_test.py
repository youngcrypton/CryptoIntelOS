from dataclasses import FrozenInstanceError, asdict
from datetime import UTC, datetime
from typing import get_type_hints
import pytest
from src.core_intelligence.policy import *
def test_policy_contracts_construct_and_serialize():
    version=PolicyVersion("1.0", datetime.now(UTC)); policy=Policy(policy_name="resolution", policy_type=PolicyType.RESOLUTION, policy_version=version, scope=PolicyScope.RESOLUTION)
    rule=PolicyRule(policy_reference=policy.policy_id, rule_name="strict", priority=1, conditions=("source_verified",), outcome="accept")
    decision=PolicyDecision(policy_reference=policy.policy_id, applied_rules=(rule.rule_id,), outcome="accept")
    assert asdict(policy)["policy_type"] is PolicyType.RESOLUTION
    assert decision.applied_rules == (rule.rule_id,)
def test_immutability_and_enums():
    with pytest.raises(FrozenInstanceError): PolicyVersion("1").version="2"
    assert PolicyStatus.ACTIVE.value == "active"
    assert PolicyScope.ORGANIZATION.value == "organization"
def test_registry_and_typing():
    assert "register" in PolicyRegistry.__dict__
    assert get_type_hints(Policy)["policy_type"] is PolicyType
