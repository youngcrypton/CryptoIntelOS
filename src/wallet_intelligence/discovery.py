from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from src.blockchain_platform.adapters import AdapterResult
from src.core_intelligence.onchain import Wallet

from .wallet_profile import WalletProfile


@dataclass(frozen=True, slots=True)
class WalletDiscoveryResult:
    profiles: tuple[WalletProfile, ...]


class WalletDiscovery:
    """Deterministically discover wallet profiles from adapter outputs."""

    def discover(
        self,
        adapter_result: AdapterResult,
        metadata: Mapping[str, Mapping[str, Any]] | None = None,
    ) -> WalletDiscoveryResult:
        metadata = metadata or {}
        profiles = tuple(self._profile(wallet, metadata.get(wallet.wallet_id, {})) for wallet in adapter_result.wallets)
        return WalletDiscoveryResult(profiles)

    @staticmethod
    def _profile(wallet: Wallet, details: Mapping[str, Any]) -> WalletProfile:
        return WalletProfile(
            wallet=wallet,
            wallet_type=str(details.get("wallet_type", "unknown")),
            ens_name=details.get("ens_name"),
        )
