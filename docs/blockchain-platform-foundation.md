# Blockchain Platform Foundation

## Platform responsibilities

The Blockchain Platform is a blockchain-agnostic infrastructure boundary shared by future Wallet Intelligence, Blockchain Intelligence, and other on-chain applications. Sprint 1 defines immutable chain descriptions, SDK collector and adapter protocols, registry behavior, validation interfaces, integration metadata, descriptive transports, and Runtime delegation.

It contains no RPC, REST, GraphQL, WebSocket, API, indexer, wallet tracking, transaction parsing, token, or contract implementation.

## Adapter architecture

`BlockchainCollector` extends the Platform SDK `SourceCollector` protocol. `BlockchainAdapter` extends `SourceAdapter[Blockchain]` and establishes the future translation boundary from infrastructure records to canonical observations. Source-specific objects must be adapted before entering Runtime.

## Capability model

`BlockchainCapability` describes smart contracts, tokens, NFTs, governance, validators, staking, decentralized exchanges, bridges, and name services. `ChainCapability` records whether a declared capability is enabled and may carry a description. Capabilities are descriptive and perform no detection or network access.

## Runtime integration

`BlockchainRuntimeIntegration` accepts only the SDK canonical output tuple and delegates through `RuntimeFacade`. Kernel, Runtime, Platform SDK, and existing intelligence applications remain unchanged.

## Future roadmap

Later sprints may add concrete chain definitions, provider selection, transport implementations, policy-aware collection, canonical adapters, blockchain discovery, and on-chain intelligence applications. Wallet, transaction, token, and contract domain models remain outside this foundation sprint.
