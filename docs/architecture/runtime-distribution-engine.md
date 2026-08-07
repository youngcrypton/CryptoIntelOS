# Runtime VII: Distribution Engine

## Distribution philosophy

The Distribution Engine transports canonical Runtime plans to destination plugins. It does not generate intelligence, evaluate automation policy, execute business rules, or format provider-specific content. Its contracts remain destination and transport agnostic.

## Provider abstraction

`DistributionProvider` defines the boundary implemented by future destination plugins. A provider accepts an immutable request and context and returns an immutable result. Discord, Telegram, desktop, email, webhook, dashboard, and REST API adapters can implement this protocol without changing Runtime contracts.

## Target model

`DistributionTarget` identifies a canonical destination and its `DistributionChannel`. Addresses and metadata remain opaque to the Runtime layer so provider plugins can interpret them without introducing source- or transport-specific dependencies.

## Strategy model

`DistributionStrategy` coordinates how a plan is delivered through a registry. Immediate, batched, scheduled, priority, broadcast, and fan-out behavior can be supplied later as plugins. `DistributionPolicy` carries retry, batching, priority, and partial-delivery settings without implementing those behaviors.

## Plugin architecture

`DistributionRegistry` resolves provider plugins by stable names. `DistributionEngine` supplies the registry, immutable plan, and immutable context to a selected strategy. The engine contains no provider implementation and no delivery business logic.

## Future transports

Transport adapters may use HTTP, queues, local desktop bridges, email infrastructure, or provider SDKs downstream. Canonical messages contain unformatted content and payload data; rendering and transport negotiation belong to provider plugins.

## Distributed execution compatibility

Plans and requests carry stable identifiers, explicit priorities, timestamps, optional scheduling data, and immutable tuple collections. Future dispatchers can serialize these contracts, partition batches, retry idempotently by request identifier, route work to remote providers, and aggregate results without redesigning the Distribution Engine.
