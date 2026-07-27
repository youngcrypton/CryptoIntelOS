from dataclasses import dataclass, field


@dataclass
class WebsiteSnapshot:
    """
    Represents a downloaded website and all of the
    intelligence extracted from it.
    """

    # Basic Information
    url: str
    title: str
    description: str
    html: str

    # SEO
    canonical_url: str = ""
    language: str = ""

    # Structured Content
    headings: list[str] = field(default_factory=list)
    meta_tags: dict[str, str] = field(default_factory=dict)

    # Links
    navigation_links: list[str] = field(default_factory=list)
    internal_links: list[str] = field(default_factory=list)
    external_links: list[str] = field(default_factory=list)

    # Media
    images: list[str] = field(default_factory=list)

    # Intelligence
    page_text: str = ""
    keywords: list[str] = field(default_factory=list)