from __future__ import annotations
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Mapping, Protocol
from src.core_intelligence.models import Observation
from src.providers.connectors import ConnectorContext, ConnectorMetadata, ConnectorPolicy, ConnectorResult
from src.providers.providers import ProviderContext, ProviderMetadata, ProviderPolicy, ProviderResult
from src.providers.adapters import AdapterContext, AdapterMetadata, AdapterResult

class ProviderIntegrationError(Exception): pass
class AuthenticationFailure(ProviderIntegrationError): pass
class RateLimitExceeded(ProviderIntegrationError): pass
class RetryableProviderError(ProviderIntegrationError): pass
class PermanentProviderError(ProviderIntegrationError): pass
class ProviderTimeout(ProviderIntegrationError): pass
class SerializationFailure(ProviderIntegrationError): pass
class TransportFailure(ProviderIntegrationError): pass
class MappingFailure(ProviderIntegrationError): pass
class CapabilityUnavailable(ProviderIntegrationError): pass
@dataclass(frozen=True, slots=True)
class GitHubConfig:
    token: str | None = None; api_version: str = "2022-11-28"; timeout_seconds: float = 30.0; page_size: int = 100
@dataclass(frozen=True, slots=True)
class GitHubConnector:
    config: GitHubConfig = field(default_factory=GitHubConfig)
    transport: Any = None
    metadata: ConnectorMetadata = field(default_factory=lambda: ConnectorMetadata("github-rest", "GitHub REST", capabilities=()))
    def request(self, operation: str, context: ConnectorContext, policy: ConnectorPolicy) -> ConnectorResult:
        if self.transport is None: raise TransportFailure("GitHub transport is not configured")
        try: payload = self.transport.request(operation, token=self.config.token, version=self.config.api_version, timeout=policy.timeout_seconds)
        except TimeoutError as error: raise ProviderTimeout(str(error)) from error
        return ConnectorResult(self.metadata.connector_id, True, payload, metadata={"api_version": self.config.api_version})
@dataclass(frozen=True, slots=True)
class GitHubProvider:
    connector: GitHubConnector
    metadata: ProviderMetadata = field(default_factory=lambda: ProviderMetadata("github", "GitHub", source="github"))
    def normalize(self, result: ConnectorResult, context: ProviderContext, policy: ProviderPolicy) -> ProviderResult:
        return ProviderResult(self.metadata.provider_id, result.success, result.payload, result.error, (("connector", result.connector_id), ("api_version", self.connector.config.api_version)))
@dataclass(frozen=True, slots=True)
class GitHubAdapter:
    metadata: AdapterMetadata = field(default_factory=lambda: AdapterMetadata("github-canonical", "GitHub Canonical Adapter"))
    def adapt(self, result: ProviderResult, context: AdapterContext) -> AdapterResult:
        payload = result.value if isinstance(result.value, Mapping) else {"value": result.value}
        now = datetime.now(UTC); identifier = str(payload.get("id", context.execution_id))
        observation = Observation(f"github:{identifier}", "github", identifier, "github-rest", now, now, "github-adapter-1", str(payload.get("sha", identifier)), payload)
        return AdapterResult(self.metadata.adapter_id, (observation,), result.provenance)
class GitHubRepositoryProvider(GitHubProvider): pass
class GitHubOrganizationProvider(GitHubProvider): pass
class GitHubUserProvider(GitHubProvider): pass
class GitHubIssueProvider(GitHubProvider): pass
class GitHubPullRequestProvider(GitHubProvider): pass
class GitHubCommitProvider(GitHubProvider): pass
class GitHubReleaseProvider(GitHubProvider): pass
class GitHubContributorProvider(GitHubProvider): pass
class GitHubWorkflowProvider(GitHubProvider): pass
class GitHubSecurityProvider(GitHubProvider): pass
class GitHubTopicProvider(GitHubProvider): pass
class GitHubBranchProvider(GitHubProvider): pass
class GitHubLanguageProvider(GitHubProvider): pass
class GitHubStatisticsProvider(GitHubProvider): pass
