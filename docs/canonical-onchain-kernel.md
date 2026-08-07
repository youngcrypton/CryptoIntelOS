# Canonical On-Chain Kernel

## Architecture

The Core Intelligence Kernel owns the canonical, blockchain-agnostic language for on-chain intelligence. The `src/core_intelligence/onchain` package defines immutable business entities for identity, transactions, assets, contracts, DeFi, governance, references, and execution context.

These models serialize through the existing Kernel `SerializableModel` contract where they carry structured intelligence data. They contain no transport, RPC, API, parsing, indexing, or provider behavior.

## Model ownership

Core Intelligence owns `Wallet`, `Address`, `ChainAccount`, `Transaction`, `Transfer`, `TransactionFee`, `Token`, `TokenBalance`, `Contract`, `ContractDeployment`, `ContractInteraction`, `NFT`, `NFTCollection`, liquidity and position models, governance models, `BlockReference`, `ChainReference`, and `OnChainContext`.

`OnChainRegistry` is protocol-only. Implementations and persistence are intentionally deferred.

## Blockchain agnosticism

Models use generic identifiers, references, assets, amounts, statuses, and relationships. They do not encode a chain vendor, address format, transaction encoding, consensus mechanism, endpoint, or provider SDK. Chain-specific interpretation belongs outside the Kernel.

## Relationship to Blockchain Platform

The Blockchain Platform Foundation owns infrastructure contracts: chain metadata, capabilities, endpoints, collectors, adapters, registries, and SDK Runtime integration. It may describe how a chain is accessed, but it does not own canonical business entities. The Core Intelligence Kernel consumes normalized canonical objects after future platform adapters translate source data.

## Future Wallet Intelligence

Future Wallet Intelligence can use `Wallet`, `Address`, `ChainAccount`, `TokenBalance`, and transaction models to represent observations, histories, relationships, and assessments without changing platform contracts. Discovery, tracking, labeling, and risk logic remain application-layer responsibilities.

## Future Blockchain Intelligence

Future Blockchain Intelligence can build analyzers for transfers, contracts, DeFi positions, governance, validators, and bridges on top of these stable models. RPC clients, indexers, chain adapters, parsing, correlation, AI, and persistence belong to later bounded components and must not be added to this kernel.
