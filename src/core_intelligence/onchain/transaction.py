from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel

from .block_reference import BlockReference
from .chain_reference import ChainReference
from .transaction_fee import TransactionFee
from .transfer import Transfer


@dataclass(frozen=True, slots=True)
class Transaction(SerializableModel):
    transaction_id: str
    chain: ChainReference
    block: BlockReference | None = None
    status: str = "unknown"
    transfers: tuple[Transfer, ...] = ()
    fee: TransactionFee | None = None
