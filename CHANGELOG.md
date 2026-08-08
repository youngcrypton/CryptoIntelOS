# Changelog

All notable changes to CryptoIntel OS are documented here.

The project follows [Semantic Versioning](https://semver.org/). Dates will be added when releases are formally tagged.

## [Unreleased]

- Public release preparation and documentation review.

## [1.2.0] — Intelligence Query Engine

### Added

- Deterministic query parsing, validation, planning, optimization, execution, and statistics.
- Filtering, projection, aggregation, sorting, ranking, pagination, time ranges, caching, and relationship traversal.
- Query, search, and explain-query CLI commands.
- Framework-neutral query API contracts and documentation.

## [1.1.0] — System Integration and Validation

### Added

- Production CLI entry point and end-to-end project profile execution.
- Reusable retry and backoff transport wrappers.
- System integration tests and benchmarking guidance.

## [1.0.0] — Live Intelligence Provider Contracts

### Added

- GitHub, Website, Ethereum, and Solana provider packages with injectable transports.
- Provider-specific connector, normalization, adapter, configuration, and deterministic fixture paths.
- Provider authentication and development documentation.

## [0.9.0] — Provider Ecosystem

### Added

- Connector, Provider, and Adapter protocols, metadata, results, contexts, health, policies, and registries.
- Provider management contracts for capability negotiation, selection, health, failover, rate limiting, retries, circuit breaking, and statistics.
- Canonical Provider-to-Platform-SDK projection boundary.

## [0.8.0] — Production Runtime Contracts

### Added

- Durable execution jobs, states, checkpoints, snapshots, replay, recovery, lifecycle, and retry contracts.
- Runtime event bus, persistence protocols, observability contracts, and provider infrastructure.

## [0.7.0] — Platform Hardening

### Changed

- Consolidated canonical model ownership.
- Enforced canonical Runtime projections and explicit type rejection.
- Redirected legacy orchestration through Platform SDK and Runtime.
- Added repository validation, complete pytest discovery, CI quality gates, and canonical Docker module startup.

## Earlier Development Releases

Earlier commits established the Core Intelligence Kernel, Runtime pipeline, Blockchain Platform, GitHub/Twitter/Website/Wallet Intelligence, Unified Intelligence fusion, and Project Intelligence Profiles.
