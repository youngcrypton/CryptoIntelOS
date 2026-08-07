from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel


@dataclass(frozen=True, slots=True)
class Swap(SerializableModel):
    swap_id: str
    pool_id: str
    trader: str
    input_asset: str
    output_asset: str
    input_amount: str
    output_amount: str
