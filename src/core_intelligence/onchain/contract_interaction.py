from dataclasses import dataclass, field
from typing import Any

from src.core_intelligence.models import SerializableModel

from .contract import Contract


@dataclass(frozen=True, slots=True)
class ContractInteraction(SerializableModel):
    interaction_id: str
    contract: Contract
    caller: str
    method: str
    arguments: tuple[Any, ...] = field(default_factory=tuple)
