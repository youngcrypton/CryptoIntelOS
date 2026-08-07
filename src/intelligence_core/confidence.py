"""Confidence primitives for intelligence signals."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ConfidenceScore:
    """Normalized confidence score in the inclusive range from zero to one."""

    value: float
    rationale: str | None = None

    def __post_init__(self) -> None:
        """Reject scores outside the normalized confidence range."""

        if not 0.0 <= self.value <= 1.0:
            raise ValueError("confidence value must be between 0.0 and 1.0")
