from collections.abc import Mapping
from typing import Any

from .label import LabelType
from .wallet_label import WalletLabel
from .wallet_profile import WalletProfile


class WalletClassifier:
    """Apply deterministic keyword rules to wallet metadata."""

    RULES = tuple((label, keywords) for label, keywords in (
        (LabelType.FOUNDER, ("founder", "co-founder")),
        (LabelType.TEAM, ("team", "employee", " contributor")),
        (LabelType.FOUNDATION, ("foundation",)),
        (LabelType.TREASURY, ("treasury", "reserve")),
        (LabelType.VC, ("venture", " vc", "capital")),
        (LabelType.SMART_MONEY, ("smart money",)),
        (LabelType.EXCHANGE, ("exchange", "cex", "dex")),
        (LabelType.BRIDGE, ("bridge",)),
        (LabelType.MARKET_MAKER, ("market maker", "liquidity provider")),
        (LabelType.MEV, ("mev", "arbitrage")),
        (LabelType.DAO, ("dao", "governance")),
    ))

    def classify(self, profile: WalletProfile, details: Mapping[str, Any] | None = None) -> tuple[WalletLabel, ...]:
        details = details or {}
        text = " ".join(str(value) for value in (profile.wallet.label, profile.ens_name, profile.wallet_type, *details.values()) if value).casefold()
        labels = tuple(WalletLabel(label, label.value, 1.0) for label, keywords in self.RULES if any(keyword in text for keyword in keywords))
        return labels or (WalletLabel(LabelType.UNKNOWN, "unknown", 0.5),)
