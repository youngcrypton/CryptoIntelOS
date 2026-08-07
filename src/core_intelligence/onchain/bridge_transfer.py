from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel

from .chain_reference import ChainReference


@dataclass(frozen=True, slots=True)
class BridgeTransfer(SerializableModel):
    transfer_id: str
    source_chain: ChainReference
    destination_chain: ChainReference
    sender: str
    recipient: str
    asset: str
    amount: str
