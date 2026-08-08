from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping
from src.core_intelligence.models import Observation
from src.providers.connectors import ConnectorContext, ConnectorMetadata, ConnectorPolicy, ConnectorResult
from src.providers.providers import ProviderContext, ProviderMetadata, ProviderPolicy, ProviderResult
from src.providers.adapters import AdapterContext, AdapterMetadata, AdapterResult
class WebsiteProviderError(Exception): pass
@dataclass(frozen=True, slots=True)
class WebsiteConfig: user_agent: str = "CryptoIntelOS/1.0"; timeout_seconds: float = 30.0; allow_redirects: bool = True
@dataclass(frozen=True, slots=True)
class HttpConnector:
    config: WebsiteConfig = field(default_factory=WebsiteConfig); transport: Any = None; metadata: ConnectorMetadata = field(default_factory=lambda: ConnectorMetadata("website-http", "Website HTTP"))
    def request(self, operation: str, context: ConnectorContext, policy: ConnectorPolicy) -> ConnectorResult:
        if self.transport is None: raise WebsiteProviderError("HTTP transport is not configured")
        return ConnectorResult(self.metadata.connector_id, True, self.transport.request(operation, timeout=policy.timeout_seconds, user_agent=self.config.user_agent))
@dataclass(frozen=True, slots=True)
class WebsiteFetcher:
    connector: HttpConnector; metadata: ProviderMetadata = field(default_factory=lambda: ProviderMetadata("website", "Website", source="website"))
    def fetch(self, url: str, context: ProviderContext) -> ProviderResult:
        result = self.connector.request(url, ConnectorContext(context.correlation_id, context.execution_id), ConnectorPolicy(self.connector.config.timeout_seconds))
        return ProviderResult(self.metadata.provider_id, result.success, result.payload, result.error, (("url", url),))
@dataclass(frozen=True, slots=True)
class WebsiteAdapter:
    metadata: AdapterMetadata = field(default_factory=lambda: AdapterMetadata("website-canonical", "Website Canonical Adapter"))
    def adapt(self, result: ProviderResult, context: AdapterContext) -> AdapterResult:
        payload = result.value if isinstance(result.value, Mapping) else {"value": result.value}; now = datetime.now(UTC); url = str(payload.get("canonical_url", payload.get("url", context.source)))
        return AdapterResult(self.metadata.adapter_id, (Observation(f"website:{url}", "website", url, "http", now, now, "website-adapter-1", str(payload.get("checksum", url)), payload),), result.provenance)
WebsiteProvider = WebsiteFetcher
