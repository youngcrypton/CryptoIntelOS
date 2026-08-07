# Twitter Intelligence Foundation

## Package responsibilities

`src.twitter_intelligence` defines the source-specific contracts required for a future Twitter integration. It owns immutable Twitter post/profile DTOs, Twitter collector and adapter protocols, integration metadata, a Runtime delegation façade, and source-specific exceptions.

The package does not call Twitter APIs, scrape pages, authenticate users, analyze content, generate findings or signals, or implement Runtime behavior.

## Platform SDK integration

`TwitterCollector` extends the SDK collector contract. `TwitterPostAdapter` and `TwitterProfileAdapter` extend the generic SDK source-adapter contract and will translate their source DTOs into canonical Kernel observations. Integration metadata declares version, capabilities, supported entity types, and observation types.

## Runtime integration

`TwitterRuntimeIntegration` accepts canonical SDK output and an existing Runtime execution context, then delegates to the SDK `RuntimeFacade`. No Runtime subsystem is duplicated or imported by the Kernel. Twitter-specific objects must not cross this boundary.

## Future roadmap

Future sprints may add API clients, authentication, pagination, rate-limit handling, concrete collectors/adapters, analyzers, evidence translation, findings, assessments, and signals. Those implementations must preserve the established SDK boundary and remain outside Kernel and Runtime packages.
