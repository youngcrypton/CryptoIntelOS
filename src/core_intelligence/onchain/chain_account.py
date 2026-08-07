from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel

from .address import Address
from .chain_reference import ChainReference


@dataclass(frozen=True, slots=True)
class ChainAccount(SerializableModel):
    account_id: str
    address: Address
    chain: ChainReference
    account_type: str = "account"
