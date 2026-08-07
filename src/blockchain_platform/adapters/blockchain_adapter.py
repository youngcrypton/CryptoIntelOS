from collections.abc import Mapping, Sequence
from typing import Any, Protocol

from src.core_intelligence.onchain import (
    Contract, LiquidityPool, NFT, Proposal, Token, Transaction, Transfer, Validator, Wallet,
)

from .adapter_context import AdapterContext
from .adapter_result import AdapterResult
from .provider import BlockchainProvider


RawRecord = Mapping[str, Any]


class BlockchainAdapter(Protocol):
    """Translate provider records into canonical on-chain Kernel models."""

    adapter_id: str

    def adapt(self, provider: BlockchainProvider, identifier: str, context: AdapterContext) -> AdapterResult: ...

    def adapt_wallet(self, value: RawRecord, context: AdapterContext) -> Wallet: ...

    def adapt_transactions(self, values: Sequence[RawRecord], context: AdapterContext) -> tuple[Transaction, ...]: ...

    def adapt_transfers(self, values: Sequence[RawRecord], context: AdapterContext) -> tuple[Transfer, ...]: ...

    def adapt_tokens(self, values: Sequence[RawRecord], context: AdapterContext) -> tuple[Token, ...]: ...

    def adapt_contracts(self, values: Sequence[RawRecord], context: AdapterContext) -> tuple[Contract, ...]: ...

    def adapt_nfts(self, values: Sequence[RawRecord], context: AdapterContext) -> tuple[NFT, ...]: ...

    def adapt_liquidity_pools(self, values: Sequence[RawRecord], context: AdapterContext) -> tuple[LiquidityPool, ...]: ...

    def adapt_proposals(self, values: Sequence[RawRecord], context: AdapterContext) -> tuple[Proposal, ...]: ...

    def adapt_validators(self, values: Sequence[RawRecord], context: AdapterContext) -> tuple[Validator, ...]: ...
