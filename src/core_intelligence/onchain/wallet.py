from dataclasses import dataclass

from src.core_intelligence.models import SerializableModel

from .address import Address


@dataclass(frozen=True, slots=True)
class Wallet(SerializableModel):
    wallet_id: str
    addresses: tuple[Address, ...] = ()
    label: str | None = None
