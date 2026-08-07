# Website Discovery Engine

## Discovery philosophy

Website Discovery is deterministic normalization of caller-supplied website resources. It creates canonical observations and explicit discovered entities while avoiding collection, crawling, HTTP requests, scraping, parsing, heuristics, AI, and intelligence interpretation.

## Supported resources

The engine supports Website, Page, Document, and Link observations. Resource helpers identify internal and external links, navigation entries, documentation, whitepapers, GitBook and blog references, roadmap, careers, team, audit, FAQ, and contact pages. Entity extraction also recognizes GitHub repositories, Twitter/X accounts, Discord invites, Telegram, LinkedIn, YouTube, Medium, email addresses, domains, logos, favicon references, and metadata.

## Entity extraction

`WebsiteEntityExtractor` uses explicit regular expressions and URL parsing only. URLs are normalized by lower-casing schemes and hostnames; emails are case-folded; GitHub repositories and Twitter account names receive stable normalized values. Named path segments and known social domains map directly to their declared entity types. No inference is performed.

## Canonical Observation mapping

Each Website, Page, Document, or Link discovery result creates one immutable Kernel `Observation` with source `website`, source-specific identifier, version `0.4.0`, checksum, and the original dataclass payload. Discovered entities remain attached to the `DiscoveryResult` for downstream Website analysis.

## Runtime integration

`WebsiteDiscoveryEngine.enter_runtime` delegates through `WebsiteRuntimeIntegration` and the Platform SDK `RuntimeFacade`. A single result forwards its observation directly. Multiple results are represented by one deterministic batch observation containing every child observation and extracted entity; the Runtime contract is unchanged and receives no source-specific models.
