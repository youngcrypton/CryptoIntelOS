from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class CorrelationRule:
    name: str
    correlation_type: str
    conditions: tuple[str, ...] = ()
    explanation: str | None = None
