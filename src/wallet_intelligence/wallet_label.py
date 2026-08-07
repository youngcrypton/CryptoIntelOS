from dataclasses import dataclass

from .label import LabelType


@dataclass(frozen=True, slots=True)
class WalletLabel:
    label_type: LabelType
    value: str
    confidence: float = 1.0
    source: str = "deterministic"
