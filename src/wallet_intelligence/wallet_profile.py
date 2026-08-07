from dataclasses import dataclass

from src.core_intelligence.onchain import Wallet

from .wallet_label import WalletLabel


@dataclass(frozen=True, slots=True)
class WalletProfile:
    wallet: Wallet
    wallet_type: str = "unknown"
    ens_name: str | None = None
    labels: tuple[WalletLabel, ...] = ()
