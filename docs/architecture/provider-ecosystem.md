# Provider Ecosystem

The Provider Ecosystem is the production abstraction layer between external services and the Platform SDK. It adds contracts only: no networking, credentials, live API integrations, or canonical business behavior are implemented here.

## Connector philosophy

Connectors represent communication capabilities such as REST, GraphQL, RPC, or HTTP. They own connector metadata, capabilities, health, request context, and connector policy. A connector returns an opaque `ConnectorResult`; it does not create canonical Kernel models.

## Provider philosophy

Providers normalize connector output into a stable provider result while preserving source/provenance metadata. Provider contracts are independent of canonical business semantics and can be backed by GitHub, chain, website, or social connectors in a future release.

## Adapter philosophy

Adapters are the only Provider Ecosystem layer allowed to create canonical Kernel objects. An adapter converts a validated `ProviderResult` into an immutable `AdapterResult` containing `Observation`, `Evidence`, `Finding`, `Assessment`, or `Signal` objects and provenance. The runtime projection requires exactly one observation and emits the existing Platform SDK `CanonicalOutput` contract.

## Management

`ProviderManager` deterministically coordinates Connector → Provider → Adapter. Registries, capability negotiation, provider selection, health tracking, failover, rate-limit, retry, circuit-breaker, metrics, and statistics are protocol/data contracts only. They do not perform network calls or sleep/retry operations.

## Runtime integration

The supported future flow is:

Connector → Provider → Adapter → Platform SDK → Production Runtime → Runtime → Compiler → Knowledge Graph → Correlation → Reasoning → Automation → Distribution.

`ProviderRuntimeProjection` bridges adapter output to the frozen SDK canonical projection. Existing Runtime and Platform SDK behavior are unchanged.

## Future live providers

Future providers must implement connector communication behind `Connector`, normalization behind `Provider`, and canonical creation behind `Adapter`. They must declare capabilities and versions, preserve source identifiers/provenance, expose health, honor rate limits, and use management policies. Networking, provider-specific retries, authentication, and external SDK dependencies belong in separately reviewed provider implementations, never in these contracts.
