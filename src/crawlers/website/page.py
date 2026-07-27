from dataclasses import dataclass


@dataclass
class CrawledPage:
    """
    Represents one crawled webpage.
    """

    url: str

    depth: int

    title: str

    description: str

    canonical_url: str

    language: str

    html: str

    text: str

    status_code: int

    headings: list

    meta_tags: dict

    navigation_links: list

    internal_links: list

    external_links: list

    images: list