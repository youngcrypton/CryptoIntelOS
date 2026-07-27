from src.collectors.base_collector import (
    BaseCollector,
)

from src.crawlers.website.crawler import (
    website_crawler,
)

from src.models.collector_result import (
    CollectorResult,
)

from src.models.website import (
    WebsiteSnapshot,
)


class WebsiteCollector(BaseCollector):
    """
    Collects intelligence from project websites.
    """

    name = "Website Collector"

    def collect(
        self,
        project,
    ):

        if not project.website:

            return None

        try:

            pages = website_crawler.crawl(
                start_url=project.website,
                max_pages=10,
                max_depth=2,
            )

            if not pages:

                raise Exception(
                    "Crawler returned no pages."
                )

            home = pages[0]

            snapshot = WebsiteSnapshot(
                url=home.url,
                title=getattr(home, "title", ""),
                description=getattr(
                    home,
                    "description",
                    "",
                ),
                html=home.html,
                canonical_url=getattr(
                    home,
                    "canonical_url",
                    "",
                ),
                language=getattr(
                    home,
                    "language",
                    "",
                ),
                headings=getattr(
                    home,
                    "headings",
                    [],
                ),
                meta_tags=getattr(
                    home,
                    "meta_tags",
                    {},
                ),
                navigation_links=getattr(
                    home,
                    "navigation_links",
                    [],
                ),
                internal_links=getattr(
                    home,
                    "internal_links",
                    [],
                ),
                external_links=getattr(
                    home,
                    "external_links",
                    [],
                ),
                images=getattr(
                    home,
                    "images",
                    [],
                ),
                page_text=getattr(
                    home,
                    "text",
                    "",
                ),
                keywords=getattr(
                    home,
                    "keywords",
                    [],
                ),
            )

            print(f"✓ {self.name}: {project.name}")

            return CollectorResult(
                project=project.name,
                collector=self.name,
                signal_type="Website",
                title="Website Collected",
                summary=f"Crawled {len(pages)} page(s).",
                confidence=100,
                evidence="Rendered using Playwright.",
                payload=snapshot,
            )

        except Exception as error:

            print(f"✗ {self.name}: {project.name}")
            print(error)

            return CollectorResult(
                project=project.name,
                collector=self.name,
                signal_type="Website",
                title="Website Collection Failed",
                summary=str(error),
                confidence=0,
                evidence="Crawler raised an exception.",
                payload=None,
            )


website_collector = WebsiteCollector()