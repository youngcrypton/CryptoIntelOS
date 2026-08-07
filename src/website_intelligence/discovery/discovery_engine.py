import hashlib
import json

from src.core_intelligence.models import Observation
from src.runtime.engine import ExecutionContext, ExecutionResult

from ..models import Document, Link, Page, Website
from ..runtime import WebsiteRuntimeIntegration
from .discovery_result import DiscoveryResult
from .document_discovery import DocumentDiscovery
from .link_discovery import LinkDiscovery
from .page_discovery import PageDiscovery
from .website_discovery import WebsiteDiscovery


class WebsiteDiscoveryEngine:
    def __init__(self) -> None:
        self.websites = WebsiteDiscovery()
        self.pages = PageDiscovery()
        self.documents = DocumentDiscovery()
        self.links = LinkDiscovery()

    def discover_website(self, website: Website) -> DiscoveryResult:
        return self.websites.discover(website)

    def discover_page(self, page: Page) -> DiscoveryResult:
        return self.pages.discover(page)

    def discover_document(self, document: Document) -> DiscoveryResult:
        return self.documents.discover(document)

    def discover_link(self, link: Link, *, base_url: str | None = None) -> DiscoveryResult:
        return self.links.discover(link, base_url=base_url)

    @staticmethod
    def enter_runtime(results: tuple[DiscoveryResult, ...], integration: WebsiteRuntimeIntegration, context: ExecutionContext) -> ExecutionResult:
        if not results:
            raise ValueError("at least one discovery result is required")
        observation = results[0].observation
        if len(results) > 1:
            payload = {
                "discovery_type": "batch",
                "results": [
                    {
                        "discovery_id": result.discovery_id,
                        "discovery_type": result.discovery_type,
                        "observation": result.observation.to_dict(),
                        "entities": [
                            {
                                "entity_type": entity.entity_type.value,
                                "value": entity.value,
                                "normalized_value": entity.normalized_value,
                            }
                            for entity in result.entities
                        ],
                    }
                    for result in results
                ],
            }
            checksum = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
            observation = Observation(
                f"website:discovery:batch:{checksum[:16]}",
                "website",
                checksum,
                "website-source",
                results[0].observation.collected_at,
                max(result.observation.observed_at for result in results),
                "0.4.0",
                checksum,
                payload,
            )
        return integration.integrate((observation, (), (), (), ()), context)
