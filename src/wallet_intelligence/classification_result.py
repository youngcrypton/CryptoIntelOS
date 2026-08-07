from dataclasses import dataclass

from .wallet_label import WalletLabel
from .wallet_profile import WalletProfile


@dataclass(frozen=True, slots=True)
class ClassificationResult:
    profile: WalletProfile
    labels: tuple[WalletLabel, ...]
