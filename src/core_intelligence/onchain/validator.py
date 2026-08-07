from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class Validator(SerializableModel):
    validator_id: str
    operator: str
    status: str = "unknown"
    voting_power: str | None = None
