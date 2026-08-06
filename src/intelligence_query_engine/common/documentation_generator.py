"""Structured documentation generator for the Intelligence Query Engine."""

from dataclasses import dataclass
from typing import Final

from src.intelligence_query_engine.knowledge_registry import knowledge_registry


@dataclass(frozen=True)
class DocumentationStatistics:
    """Counts and supported capabilities of the Intelligence Query Engine."""

    builder_count: int
    knowledge_pack_count: int
    supported_intelligence_sources: list[str]
    supported_query_categories: list[str]


@dataclass(frozen=True)
class IQEDocumentation:
    """Structured overview of IQE knowledge, builders, and processing."""

    registered_ecosystems: list[str]
    registered_domains: list[str]
    total_knowledge_packs: int
    builders: list[str]
    processing_components: list[str]
    statistics: DocumentationStatistics
    architecture_summary: str


class IQEDocumentationGenerator:
    """Generate a concise, current documentation snapshot of IQE."""

    _BUILDERS: Final[list[str]] = [
        "WebsiteQueryBuilder",
        "GoogleDorkBuilder",
        "LaunchpadQueryBuilder",
        "WalletQueryBuilder",
        "AIQueryBuilder",
    ]
    _PROCESSING_COMPONENTS: Final[list[str]] = [
        "QueryValidator",
        "QueryProcessingPipeline",
    ]
    _INTELLIGENCE_SOURCES: Final[list[str]] = [
        "Twitter",
        "Websites",
        "Google",
        "Launchpads",
        "Wallets",
    ]
    _QUERY_CATEGORIES: Final[list[str]] = [
        "twitter",
        "websites",
        "google",
        "launchpads",
        "wallets",
        "funding",
        "partnerships",
        "governance",
        "documentation",
        "audits",
        "developers",
        "ecosystem",
    ]

    def generate(self) -> IQEDocumentation:
        """Return a structured snapshot of the current IQE architecture."""

        ecosystems = knowledge_registry.get_ecosystems()
        domains = knowledge_registry.get_domains()
        ecosystem_names = sorted(ecosystems)
        domain_names = self._domain_names(domains)
        knowledge_pack_count = len(ecosystem_names) + len(domain_names)

        return IQEDocumentation(
            registered_ecosystems=ecosystem_names,
            registered_domains=domain_names,
            total_knowledge_packs=knowledge_pack_count,
            builders=list(self._BUILDERS),
            processing_components=list(self._PROCESSING_COMPONENTS),
            statistics=DocumentationStatistics(
                builder_count=len(self._BUILDERS),
                knowledge_pack_count=knowledge_pack_count,
                supported_intelligence_sources=list(self._INTELLIGENCE_SOURCES),
                supported_query_categories=list(self._QUERY_CATEGORIES),
            ),
            architecture_summary=self._architecture_summary(),
        )

    @staticmethod
    def _domain_names(domains: dict[str, dict[str, object]]) -> list[str]:
        """Flatten registered domain groups into stable domain identifiers."""

        return sorted(
            f"{group}.{domain}"
            for group, grouped_domains in domains.items()
            for domain in grouped_domains
        )

    @staticmethod
    def _architecture_summary() -> str:
        """Describe the IQE composition in concise prose."""

        return (
            "CryptoIntel OS separates curated ecosystem and domain knowledge "
            "packs from reusable discovery builders. Builders generate source-"
            "specific queries, AIQueryBuilder orchestrates them into a unified "
            "plan, and validation and processing components normalize and score "
            "the resulting intelligence queries."
        )
