# System Integration

The validation path is Connector → Provider → Adapter → Platform SDK → Production Runtime → Runtime pipeline → Project Intelligence Profile. The CLI uses deterministic provider-shaped input and the existing Unified Intelligence profile builder, allowing end-to-end validation without external connectivity.

`src.providers.transports` supplies reusable retry/backoff transport wrappers for future HTTP and JSON-RPC implementations. Credentials and network clients remain injectable; no secrets are hardcoded.
