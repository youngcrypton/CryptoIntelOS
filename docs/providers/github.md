# GitHub Live Provider

The GitHub provider uses a configurable personal access token, API version, timeout, and mockable transport. Repository, organization, user, issue, pull request, commit, release, contributor, workflow, security, topic, branch, language, and statistics provider roles share the same connector/provider contracts. No network call is made without an injected transport.

Connector output remains opaque; the adapter creates the canonical observation and preserves provider/API provenance. Pagination, conditional requests, retry/backoff, rate limiting, health, metrics, and tracing are represented by the shared ecosystem contracts and belong in a future transport implementation.
