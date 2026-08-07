"""Configurable, declarative resolution policy contract."""
from dataclasses import dataclass
from enum import StrEnum

class ResolutionPolicyMode(StrEnum):
    STRICT = "strict"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"
    MANUAL_REVIEW = "manual_review"

@dataclass(frozen=True, slots=True)
class ResolutionPolicy:
    name: str
    mode: ResolutionPolicyMode = ResolutionPolicyMode.BALANCED
    version: str = "1"
    metadata: tuple[tuple[str, str], ...] = ()
