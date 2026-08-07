# Website Intelligence Foundation

## Package responsibilities

`src.website_intelligence` defines the source boundary for website-derived intelligence. Sprint 1 contains immutable source models, Platform SDK collector and adapter protocols, integration metadata, package exports, source-specific exceptions, and a Runtime integration facade. It deliberately contains no collection or interpretation behavior.

## Website Intelligence role

Official websites and their published pages and documents provide authoritative project names, domains, descriptions, and documentation references. Website Intelligence is designed to become the identity anchor that future correlation can connect to Twitter, GitHub, and other sources while retaining canonical provenance.

The foundation represents four source concepts:

- `Website`: the official site identity and domain.
- `Page`: a page belonging to a website.
- `Link`: an explicit relationship from a page to another URL.
- `Document`: a published artifact such as documentation or a whitepaper.

## SDK integration

`WebsiteCollector` derives from the Platform SDK `SourceCollector` protocol. `WebsiteAdapter`, `PageAdapter`, `LinkAdapter`, and `DocumentAdapter` derive from the generic `SourceAdapter` protocol. Future implementations must translate source objects into canonical observations before they cross the package boundary.

`WEBSITE_INTEGRATION_METADATA` declares version `0.4.0`, source capabilities, supported entity types, and supported observation types through the SDK `IntegrationMetadata` contract.

## Runtime integration

`WebsiteRuntimeIntegration` accepts only the SDK canonical output tuple and delegates it to `RuntimeFacade`. Runtime, Kernel, Platform, and SDK components remain unchanged, and no Website-specific object enters Runtime.

## Future implementation roadmap

Later sprints may add policy-aware collection, URL and page discovery, robots.txt handling, HTTP retrieval, parsing, document classification, canonical adapters, deterministic analysis, correlation, and signals. These capabilities should build behind the contracts established here. Sprint 1 performs no crawling, HTTP requests, scraping, parsing, or business logic.
