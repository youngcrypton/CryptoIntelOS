# Blockchain Adapter SDK

## Provider architecture

`BlockchainProvider` defines protocol-only discovery methods for raw wallet, transaction, contract, token, NFT, protocol, and governance records. Providers own acquisition of raw blockchain data. Sprint 3 supplies no networking, RPC, API, parsing, or provider implementation.

`ProviderMetadata` declares provider identity, version, supported chains, and descriptive capabilities. `ProviderRegistry` stores provider protocol implementations by stable provider identifier.

## Adapter architecture

`BlockchainAdapter` consumes a provider and translates provider-neutral mappings into canonical models owned by `src.core_intelligence.onchain`. Its typed conversion methods cover wallets, transactions, transfers, tokens, contracts, NFTs, liquidity pools, proposals, and validators. `AdapterContext` carries provider, chain, observation, and correlation references; `AdapterResult` groups canonical outputs.

`AdapterRegistry` stores adapters by stable adapter identifier. Ethereum, generic EVM, and Solana adapters are protocol stubs only.

## Provider and adapter responsibilities

Providers obtain raw records and expose provider metadata. Adapters interpret those records and construct canonical Kernel models. Applications depend on adapter contracts and canonical results rather than provider schemas. This separation prevents Wallet Intelligence and other applications from coupling to a particular chain or data vendor.

## Future chain expansion

Future EVM-compatible chains can implement or extend `EVMAdapter`; Ethereum implementations can satisfy `EthereumAdapter`. Non-EVM chains can implement `BlockchainAdapter` directly, as represented by `SolanaAdapter`. Concrete providers, validation, error translation, parsing, retries, rate limiting, and network transports belong to later sprints.
