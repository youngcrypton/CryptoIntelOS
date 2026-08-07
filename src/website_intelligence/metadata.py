from src.platform_sdk import IntegrationMetadata


WEBSITE_INTEGRATION_METADATA = IntegrationMetadata(
    collector="WebsiteCollector",
    source="website",
    adapter="WebsiteAdapter,PageAdapter,LinkAdapter,DocumentAdapter",
    version="0.4.0",
    capabilities=("websites", "pages", "links", "documents"),
    supported_entity_types=("organization", "project", "website", "document"),
    supported_observation_types=(
        "website",
        "website_page",
        "website_link",
        "website_document",
    ),
)
