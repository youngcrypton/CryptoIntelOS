from dataclasses import dataclass

from src.core_intelligence.onchain import (
    Contract, LiquidityPool, NFT, Proposal, Token, Transaction, Transfer, Validator, Wallet,
)


@dataclass(frozen=True, slots=True)
class AdapterResult:
    wallets: tuple[Wallet, ...] = ()
    transactions: tuple[Transaction, ...] = ()
    transfers: tuple[Transfer, ...] = ()
    tokens: tuple[Token, ...] = ()
    contracts: tuple[Contract, ...] = ()
    nfts: tuple[NFT, ...] = ()
    liquidity_pools: tuple[LiquidityPool, ...] = ()
    proposals: tuple[Proposal, ...] = ()
    validators: tuple[Validator, ...] = ()
